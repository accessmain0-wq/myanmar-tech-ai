// api/proxy.js — Facebook Video Download Proxy
// Deploy to Vercel as a Serverless Function

export default async function handler(req, res) {
  // CORS headers — allow any origin to use this proxy
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }
  
  const { url, quality } = req.query;
  
  if (!url) {
    return res.status(400).json({ 
      error: 'Missing url parameter',
      usage: `${req.headers.host}/api/proxy?url=VIDEO_URL&quality=hd`
    });
  }
  
  // Validate URL
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    return res.status(400).json({ error: 'Invalid URL' });
  }
  
  try {
    console.log(`[PROXY] Fetching: ${url.substring(0, 80)}...`);
    
    // Fetch the video from Facebook CDN
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'video/mp4,video/*;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.facebook.com/',
        'Origin': 'https://www.facebook.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'video',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site'
      }
    });
    
    if (!response.ok) {
      console.error(`[PROXY] Facebook responded with ${response.status}`);
      return res.status(502).json({ 
        error: `Facebook CDN responded with ${response.status}`,
        message: 'The video URL may have expired. Please extract again.'
      });
    }
    
    // Get content type from Facebook
    const contentType = response.headers.get('content-type') || 'video/mp4';
    
    // Set FORCE DOWNLOAD headers
    const filename = `facebook_video_${quality || 'hd'}_TZP_${Date.now()}.mp4`;
    res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
    res.setHeader('Content-Type', contentType);
    res.setHeader('Content-Length', response.headers.get('content-length') || '');
    res.setHeader('Cache-Control', 'no-cache, no-store, must-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    
    // Stream the video to the client
    const reader = response.body.getReader();
    const stream = new ReadableStream({
      async pull(controller) {
        const { done, value } = await reader.read();
        if (done) {
          controller.close();
          return;
        }
        controller.enqueue(value);
      }
    });
    
    // Pipe the stream
    return new Response(stream, {
      headers: res.getHeaders()
    });
    
  } catch (error) {
    console.error(`[PROXY] Error: ${error.message}`);
    return res.status(500).json({ 
      error: 'Proxy fetch failed',
      message: error.message
    });
  }
}
