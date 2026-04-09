<!DOCTYPE html>
<html lang="my">
<head>
<meta charset="UTF-8">
<title>စာရင်းများ</title>
<style>
    body {
        font-family: sans-serif;
        padding: 20px;
    }
    h2 {
        text-align: center;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        text-align: center;
    }
    th, td {
        border: 1px solid #999;
        padding: 10px;
    }
    th {
        background-color: #f2f2f2;
    }
    .status {
        color: black;
    }
    .btn {
        margin-top: 20px;
        padding: 10px 20px;
        border: none;
        color: white;
        cursor: pointer;
        font-size: 16px;
    }
    .print {
        background-color: #555;
    }
    .save {
        background-color: green;
    }
</style>
</head>
<body>

<h2>စာရင်းများ</h2>

<table>
    <tr>
        <th>စဉ်</th>
        <th>အမည်</th>
        <th>ရက်စွဲ</th>
        <th>အခြေအနေ</th>
    </tr>

    <!-- Row Example -->
    <script>
        for(let i = 1; i <= 10; i++) {
            document.write(`
                <tr>
                    <td>${i}</td>
                    <td>...</td>
                    <td>...</td>
                    <td class="status">ပို့ပြီး</td>
                </tr>
            `);
        }
    </script>
</table>

<button class="btn print" onclick="window.print()">Print ထုတ်ရန်</button>
<button class="btn save">Data သိမ်းဆည်းရန်</button>

</body>
</html>