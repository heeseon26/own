<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>OWM Influencer Desk</title>
  <style>
    :root{
      --bg:#f5f2ed;
      --panel:#ffffff;
      --ink:#222222;
      --muted:#736f69;
      --line:#e9e4dd;
      --dark:#222222;
      --dark-2:#30302f;
      --pink:#efb6c6;
      --pink-strong:#d56f8f;
      --pink-soft:#fff0f4;
      --cream:#f3eadc;
      --green:#6f9375;
      --orange:#c68a50;
      --red:#ba5b5b;
      --shadow:0 12px 35px rgba(36,31,27,.08);
      --radius:22px;
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family:Pretendard,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Noto Sans KR",sans-serif;
      color:var(--ink);
      background:var(--bg);
    }
    button,input,select,textarea{font:inherit}
    button{cursor:pointer}
    a{color:inherit}
    .app{
      min-height:100vh;
      display:grid;
      grid-template-columns:260px 1fr;
    }
    .sidebar{
      background:linear-gradient(180deg,var(--dark),#191919);
      color:#fff;
      padding:28px 18px;
      position:sticky;
      top:0;
      height:100vh;
      display:flex;
      flex-direction:column;
      z-index:20;
    }
    .brand{
      display:flex;
      align-items:center;
      gap:12px;
      padding:4px 10px 24px;
      border-bottom:1px solid rgba(255,255,255,.1);
    }
    .brand img{
      width:70px;
      height:52px;
      object-fit:contain;
    }
    .brand-copy strong{display:block;font-size:16px;letter-spacing:.02em}
    .brand-copy span{display:block;color:#cfcfcf;font-size:12px;margin-top:4px}
    .nav{
      display:flex;
      flex-direction:column;
      gap:8px;
      margin-top:26px;
    }
    .nav button{
      border:0;
      background:transparent;
      color:#d6d6d6;
      text-align:left;
      padding:13px 14px;
      border-radius:14px;
      display:flex;
      align-items:center;
      gap:11px;
      font-weight:700;
    }
    .nav button:hover{background:rgba(255,255,255,.07);color:#fff}
    .nav button.active{
      background:#fff;
      color:#222;
      box-shadow:0 8px 18px rgba(0,0,0,.18);
    }
    .nav .icon{width:23px;text-align:center;font-size:18px}
    .side-note{
      margin-top:auto;
      padding:16px;
      border:1px solid rgba(255,255,255,.12);
      background:rgba(255,255,255,.06);
      border-radius:16px;
      color:#d8d8d8;
      font-size:12px;
      line-height:1.6;
    }
    .main{min-width:0}
    .topbar{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:16px;
      padding:24px 34px 12px;
    }
    .topbar h1{margin:0;font-size:28px;letter-spacing:-.03em}
    .topbar p{margin:7px 0 0;color:var(--muted);font-size:14px}
    .top-actions{display:flex;gap:10px;flex-wrap:wrap}
    .content{padding:16px 34px 44px}
    .page{display:none}
    .page.active{display:block}
    .grid{display:grid;gap:18px}
    .stats{grid-template-columns:repeat(4,minmax(0,1fr))}
    .stat{
      background:var(--panel);
      border:1px solid var(--line);
      border-radius:20px;
      padding:20px;
      box-shadow:var(--shadow);
    }
    .stat .label{font-size:13px;color:var(--muted);font-weight:700}
    .stat .value{font-size:31px;font-weight:800;margin-top:11px;letter-spacing:-.04em}
    .stat .sub{font-size:12px;color:var(--muted);margin-top:7px}
    .stat.pink{background:linear-gradient(135deg,#fff,#fff1f5)}
    .stat.dark{background:linear-gradient(135deg,#2d2d2d,#1d1d1d);color:#fff;border-color:#2d2d2d}
    .stat.dark .label,.stat.dark .sub{color:#cfcfcf}
    .panel{
      background:var(--panel);
      border:1px solid var(--line);
      border-radius:var(--radius);
      box-shadow:var(--shadow);
      padding:22px;
    }
    .panel + .panel{margin-top:18px}
    .panel-head{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:14px;
      margin-bottom:18px;
    }
    .panel-head h2,.panel-head h3{margin:0;letter-spacing:-.02em}
    .panel-head h2{font-size:21px}
    .panel-head h3{font-size:17px}
    .panel-head p{margin:5px 0 0;color:var(--muted);font-size:13px}
    .btn{
      border:0;
      border-radius:13px;
      padding:11px 15px;
      font-weight:800;
      display:inline-flex;
      align-items:center;
      justify-content:center;
      gap:8px;
      transition:.15s ease;
      white-space:nowrap;
    }
    .btn:hover{transform:translateY(-1px)}
    .btn-primary{background:var(--dark);color:#fff}
    .btn-pink{background:var(--pink-strong);color:#fff}
    .btn-soft{background:var(--pink-soft);color:#9c4864}
    .btn-ghost{background:#fff;color:#444;border:1px solid var(--line)}
    .btn-danger{background:#fff0f0;color:var(--red);border:1px solid #f2dada}
    .btn-sm{padding:8px 10px;font-size:12px;border-radius:10px}
    .two-col{grid-template-columns:minmax(0,1.25fr) minmax(300px,.75fr)}
    .search-wrap{
      display:flex;
      gap:10px;
      align-items:center;
      padding:9px;
      background:#f8f6f3;
      border:1px solid var(--line);
      border-radius:16px;
    }
    .search-wrap input{
      flex:1;
      min-width:0;
      border:0;
      outline:0;
      background:transparent;
      padding:7px 9px;
      font-size:16px;
    }
    .search-tip{font-size:12px;color:var(--muted);margin:10px 2px 0}
    .result-area{margin-top:18px}
    .empty{
      border:1px dashed #d8d1c8;
      background:#fbfaf8;
      border-radius:18px;
      padding:34px 18px;
      text-align:center;
      color:var(--muted);
    }
    .empty .emoji{font-size:34px;margin-bottom:10px}
    .match-card{
      border:1px solid var(--line);
      border-radius:18px;
      padding:18px;
      margin-top:12px;
      background:#fff;
    }
    .match-card:first-child{margin-top:0}
    .match-top{
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:16px;
    }
    .identity{display:flex;gap:13px;align-items:center;min-width:0}
    .avatar{
      width:45px;height:45px;border-radius:15px;
      display:grid;place-items:center;
      background:var(--pink-soft);
      color:#ad5774;
      font-weight:900;
      flex:0 0 auto;
    }
    .identity h3{margin:0;font-size:17px}
    .identity p{margin:5px 0 0;color:var(--muted);font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:420px}
    .badge{
      display:inline-flex;align-items:center;gap:6px;
      padding:6px 9px;border-radius:999px;font-size:11px;font-weight:800;
    }
    .badge.upcoming{background:#fff4df;color:#9b6a1e}
    .badge.progress{background:#eef4ff;color:#4c6f9e}
    .badge.done{background:#eaf5ec;color:#4d7655}
    .badge.cancel{background:#fff0f0;color:#a54f4f}
    .detail-grid{
      display:grid;
      grid-template-columns:repeat(3,minmax(0,1fr));
      gap:12px;
      margin-top:16px;
    }
    .detail{
      background:#f8f6f3;
      border-radius:13px;
      padding:11px 12px;
      min-width:0;
    }
    .detail span{display:block;color:var(--muted);font-size:11px;margin-bottom:5px}
    .detail strong{font-size:13px;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
    .card-actions{display:flex;gap:9px;flex-wrap:wrap;margin-top:15px}
    .workflow{
      display:grid;
      grid-template-columns:repeat(4,minmax(0,1fr));
      gap:10px;
    }
    .workflow .step{
      border:1px solid var(--line);
      background:#fbfaf8;
      border-radius:16px;
      padding:16px 13px;
      min-height:130px;
    }
    .step .num{
      width:29px;height:29px;border-radius:10px;background:var(--dark);color:#fff;
      display:grid;place-items:center;font-weight:900;font-size:12px;
    }
    .step h4{margin:15px 0 7px;font-size:14px}
    .step p{margin:0;color:var(--muted);font-size:12px;line-height:1.55}
    .form-grid{
      display:grid;
      grid-template-columns:repeat(2,minmax(0,1fr));
      gap:14px;
    }
    .field{min-width:0}
    .field.full{grid-column:1/-1}
    .field label{
      display:block;
      font-size:12px;
      font-weight:800;
      color:#5c5752;
      margin-bottom:7px;
    }
    .field input,.field select,.field textarea{
      width:100%;
      border:1px solid var(--line);
      border-radius:13px;
      background:#fff;
      padding:11px 12px;
      outline:0;
      color:var(--ink);
    }
    .field textarea{min-height:92px;resize:vertical}
    .field input:focus,.field select:focus,.field textarea:focus{
      border-color:var(--pink-strong);
      box-shadow:0 0 0 3px rgba(213,111,143,.12);
    }
    .checkline{display:flex;align-items:center;gap:9px;margin-top:7px}
    .checkline input{width:17px;height:17px;accent-color:var(--pink-strong)}
    .filters{
      display:flex;
      gap:9px;
      flex-wrap:wrap;
      align-items:center;
      margin-bottom:14px;
    }
    .filters input,.filters select{
      border:1px solid var(--line);
      background:#fff;
      border-radius:12px;
      padding:10px 11px;
      outline:0;
    }
    .filters input{min-width:230px;flex:1}
    .table-wrap{
      overflow:auto;
      border:1px solid var(--line);
      border-radius:16px;
    }
    table{
      width:100%;
      border-collapse:collapse;
      min-width:1200px;
      background:#fff;
    }
    th,td{
      padding:12px 11px;
      border-bottom:1px solid var(--line);
      text-align:left;
      font-size:12px;
      vertical-align:middle;
      white-space:nowrap;
    }
    th{
      position:sticky;top:0;z-index:1;
      background:#f5f2ed;
      color:#5f5a55;
      font-size:11px;
      text-transform:none;
    }
    td .account{
      max-width:190px;
      display:block;
      overflow:hidden;
      text-overflow:ellipsis;
    }
    tr:last-child td{border-bottom:0}
    tr:hover td{background:#fffafc}
    .row-actions{display:flex;gap:6px}
    .log-list{display:flex;flex-direction:column;gap:11px}
    .log-item{
      display:grid;
      grid-template-columns:48px 1fr auto;
      gap:13px;
      align-items:center;
      border:1px solid var(--line);
      border-radius:15px;
      padding:13px;
    }
    .log-icon{
      width:42px;height:42px;border-radius:13px;
      display:grid;place-items:center;
      background:#f5f2ed;
      font-size:18px;
    }
    .log-main strong{display:block;font-size:14px}
    .log-main span{display:block;font-size:12px;color:var(--muted);margin-top:4px}
    .log-time{text-align:right;font-size:11px;color:var(--muted)}
    .notice{
      border-radius:16px;
      padding:14px 16px;
      background:var(--pink-soft);
      color:#84455a;
      font-size:13px;
      line-height:1.6;
      margin-bottom:16px;
    }
    .mini-list{display:flex;flex-direction:column;gap:10px}
    .mini-row{
      display:flex;align-items:center;justify-content:space-between;gap:12px;
      padding:12px 0;border-bottom:1px solid var(--line);
    }
    .mini-row:last-child{border-bottom:0}
    .mini-row strong{font-size:13px}
    .mini-row span{font-size:11px;color:var(--muted);display:block;margin-top:4px}
    .toast{
      position:fixed;right:24px;bottom:24px;z-index:100;
      background:#222;color:#fff;border-radius:14px;
      padding:13px 16px;font-size:13px;font-weight:700;
      box-shadow:0 12px 35px rgba(0,0,0,.22);
      opacity:0;transform:translateY(12px);pointer-events:none;
      transition:.2s ease;
    }
    .toast.show{opacity:1;transform:translateY(0)}
    .modal-backdrop{
      position:fixed;inset:0;background:rgba(0,0,0,.48);
      display:none;align-items:center;justify-content:center;
      padding:22px;z-index:80;
    }
    .modal-backdrop.open{display:flex}
    .modal{
      width:min(900px,100%);
      max-height:90vh;
      overflow:auto;
      background:#fff;
      border-radius:24px;
      padding:22px;
      box-shadow:0 30px 80px rgba(0,0,0,.28);
    }
    .modal-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:17px}
    .modal-head h2{margin:0;font-size:20px}
    .close{
      width:38px;height:38px;border:0;border-radius:12px;background:#f3f0ec;font-size:20px;
    }
    .modal-actions{display:flex;justify-content:flex-end;gap:9px;margin-top:18px}
    .mobile-menu{display:none}
    .muted{color:var(--muted)}
    .danger-text{color:var(--red)}
    .nowrap{white-space:nowrap}
    .pill{
      padding:5px 8px;border-radius:999px;background:#f3f0ec;font-size:11px;font-weight:700;color:#666;
    }
    @media (max-width:1050px){
      .app{grid-template-columns:84px 1fr}
      .sidebar{padding:24px 10px}
      .brand-copy,.nav .label,.side-note{display:none}
      .brand{justify-content:center;padding-left:0;padding-right:0}
      .brand img{width:58px}
      .nav button{justify-content:center;padding:13px 8px}
      .stats{grid-template-columns:repeat(2,minmax(0,1fr))}
      .two-col{grid-template-columns:1fr}
      .workflow{grid-template-columns:repeat(2,minmax(0,1fr))}
    }
    @media (max-width:720px){
      .app{display:block}
      .sidebar{
        position:fixed;left:-280px;width:260px;transition:.2s ease;
      }
      .sidebar.open{left:0}
      .brand-copy,.nav .label,.side-note{display:block}
      .nav button{justify-content:flex-start}
      .topbar{padding:18px 18px 8px}
      .content{padding:12px 18px 34px}
      .mobile-menu{display:inline-flex}
      .topbar h1{font-size:23px}
      .top-actions .hide-mobile{display:none}
      .stats,.workflow,.form-grid,.detail-grid{grid-template-columns:1fr}
      .field.full{grid-column:auto}
      .match-top{flex-direction:column}
      .log-item{grid-template-columns:42px 1fr}
      .log-time{grid-column:2;text-align:left}
    }
  </style>
</head>
<body>
<div class="app">
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQMAAADBCAYAAADLhtXAAAATPUlEQVR4nO3deZhddX3H8fcsmUASliwQIYCsmoCpCfseFqGAlEVAsRZsn5r6FITSlkpYijuosS0UF6Q8BQRtKwpCRQiWRUQQKJuUTXbKZpGEkISQTMivf3x/98lkMnfO93fuueecO/m8nuc+GZjfPefMzLmf+9tvVwgBEZHuqi9AROpBYSAigMJARCKFgYgACgMRiRQGIgIoDEQkUhiICKAwEJFIYSAigMJARCKFgYgACgMRiRQGIgIoDEQkUhiICKAwEJFIYSAigMJARCKFgYgACgMRiRQGIgIoDEQkKiMM5gMnAOuVcC6RkWYy8Hng6+0+URlhMB64ELgE2KWE84mMBBOAY4DrgM8B67T7hL3tPkE0HjgeC4NrgfOABSWdW6TTbIm9Rg4GJpZ10rL7DLYBTgfuAo4Aeko+v0hddWHv/kcDzwEfp8QggOo6EKdi1Z9/AnZEoSBrt1HAkcBNwDVVXURZzYRmTsGqQlcDlwHPVns5IqWbBZwE7AVMqfJC6jC0+H5gDnAP1mu6QaVXI1KODbD7/cfAR6k4CKD6mkFDLzAJ6zX9IDAXeBx1MsrI0gtsARwK/DXWh1YbdQmDgY4CDsdGHX6EJee7VV6QSAF6gbOw+/uD1KNWvpraXVDUCxyHzU34DXBQtZcj0pKDsPv4bGAmNX3d1fKiBtgA2B64GZgHzADGVXlBIk7jsPt1Hnb/TgP6qrygLHVsJjRzcHxciTUhbgaWVHpFImvaCguBo7Fp+B2jk8Kg4QTgMOBR4HxsbFakau8FPgMciHUSljphqAidGAZgv+h94+N+4ETgKWAFECq8Llm7dAOjgZOBM7ARsY7VqWEw0E5YLeFp4CLg58Bv0QiEtE8vsDM2a/BYYNtqL6cYIyEMGrYFvgH8DxYOFwH3VnpFMtJMBv4YW3C3B7agaMQYSWEANsd7ZnwcCfwvtvrr+1VelIwIfwPMBram5qMCeXWF0PYmdh3a8MuxGV93YyvC3qz0aqQTTAamA7sB51J9AFwEnNrOE4y0mkEzfcC3sOnN84BfY0OTjU5HEbDXwz7xsRvWFBhf6RWVaG2pGQy2DHgVeBi4ALi9youRym2BTW77BjZStRH1W1avmkGbjMY6f7bE+hbeAC4FvgMsxpoRGo0YudbFZrc2agGnVHs59bC21gyaWQk8AFyPNSF+Cbxc6RVJUcZi/QCHYbWAP8Q6AzuFagYl68bGj3fGagiPYbs7Xww8CTxR3aVJTrsAmwKnYbWBmZVeTY0pDJobB+wavz4k/nsDcBW2MxNYTaKTaj4jXRcW6PsAu2P7bXbctOCqqJmQ32PYXgsPA69gW7b9HvU1lKkHq/pPxbYW3xX4MNYMGGnUTKix7Vl1072EzXp8DWtO3IT1OSyu5tJGtGnYLsKfwHr9p2BV/wlVXtRIoDAoxmbxAdCPLVrpB94GPg0sBe5EtYY8erDNQY7F3vVHY02BcdRv+K+jKQyKN4rVN3W9ccDXz2CdkUuB+7AJT68A72BzH5aWdI11Mhb7nY1hVaDui3XiHk31M//WGgqDcm2DbfbasBz4BTZisQB4HWtaXBe/38/I2j5+a+yFD1bNB3gPsD6wMbB/FRclRmFQrT7W3N9xBda0AButWBS/XoJtqNlwF/VsduzG6u/m52Hv/mAfvtvYaq+TxvjXCgqD+uml+QvljmGe9yrWV9HMU9gqzlSbA9s1+d4x2E7WaruPAAqDkWMT4HtVX4R0rrrvjiwiJVEYiAigMBCRSGEgIoDCQEQihYGIAAoDEYkUBiICKAxEJFIYiAigMBCRSGEgIoDCQEQihYGIAAoDEYkUBiICKAxEJFIYiAigMBCRSGEgIoDCQEQihYGIAAoDEYkUBiICKAxEJFIYiAigMBCRSGEgIoDCQEQihYGIAAoDEYkUBiICKAxEJFIYiAigMBCRSGEgIoDCQEQihYGIAAoDEYkUBiICKAxEJFIYiAigMBCRSGEgIoDCQEQihYGIAAoDEYkUBiICKAxEJFIYiAigMBCRSGEgIoDCQEQihYGIAAoDEYkUBiICKAxEJOot4RyXl3AOkZHunnafoCuE0O5zrNPuE4isBVbER9uUEQYi0gHUZyAigMJARCKFgYgACgMRiRQGIgIoDEQkUhiICKAwEJFIYSAigMJARCKFgYgACgMRicpYwly2bYDPAROG+N6TwBygv9QrEukAnb5qcSowGjgJOATYwvm8FcBLwGfiv68Ar7fjAjNMBjZzln0SWJzjHDOAnmG+Px94LsdxASZiv3NPDfNFyv0d7+Qs9wSwJMfxJ2E/e5ejbN6/XblCCJ342CGEcGYI4cUQwqLQmkUhhJ+FEE6q4Of424TrnJXj+D0hhLcyjvtICGF6zus/PYTwjvP6j8t5jrwPr3NyHv+UEEK/8xyzSv7Zcz06sc/ge8D1wBeBzYFxLR5vHHAoMBfbTWZ2i8dLcR3wqLPs13Icv4fsd64PANNzHBtgY2CUs6z35yzCqQllPwJMSTz+BOBw/M3sGYnHr0Sn9Bl0AxsC1wCz2nSOMcCurPrD/RBY2KZzNTwH/N5Zdsccx78cX1iOx0Ijpc04ClgPXxNhEbA04ditOiSh7PuAg0jbnm9DYM+E8lsmlK1Mp9QM9gL+i/YFwUB9wCXAj4FpbT7Xu8CtzrKjSPv5e/D/fb8JjE04NsBuwJ85y87F+gzKMj6h7Fis0znljXEv0mqkWyWUrUwnhMFOwHeBmSWf90DsRbJ9m8/zrwllU5oKe8eH13CdjM3Ke19AS7HgK8t2ieU/CWyaUD61yXZQYvlK1D0MdgR+QfvfoZs5ALgI6zVvl5cSym7jLNeFVU1T2sLzE8o2eALkbuDiHMduRV9i+c2B3Z1lZwObJB5/TGL5StQ5DKYBl5JefS3aAcAVbT7H8c5y6+Jrf3aT3sfQTdr98DNnuZWUWyuYTb4dufd1ltsnx7EBjs75vNLUNQx6gGOBHaq+kOhDWFWyXe50lhsN/Lmj3Aak9ag3nJZQ1vuCu55yOw8n4xv7H+xkbN7KcHYlf5V/Us7nlaauYfBh4AzSq3sDnTjo8Z0WjjUa+AqwfwvHGI531KIXX80g72dV/BH2Qsp6MV2I/965Kue15DWF/Pf1mRnf/xD5m4wfz/m80tQxDMYCF5DePFiMDQfOxELkykGPk7ChsL2Ax0ifdfYe4Aj84+op3sb/Tj4BG9pqpgt4Oed1rIfNHdg4o9xxCcd8Jee15LU++e/rPWkepOtgQZz3779zzueVpo5hsDfpQzG3YlXcjwEP0XztwWLgrniOOaR1mvUAR9KezsyVwJvOsvsD+w3z/VY+wWon4E/iYzjeDrFvtXAteUzGQruV5x/T5Hs70Fq7v4vWrq3t6hgG3rHrhruxd/2UIboFWLPhI4nn2oK0MewUtwF3OMr1Yc2WZi5o8Tq6GL6pcBzWkenx5RavJdVU4P0tPH89rE9gqFrpUbTW7u+hulExl7qFwY74F5iAvaiPxxaCpK64ehcbttwDWO58Tg821NgOC+LDcw0bMPSLtZfsTrAsc+Oj2Vj9ofjmFyyKjzKNZvig9JiMhcJg+7V43G6qHxkbVt3CYBOszed1Lq3PbHsE+LeE8t6x/lRLsCaO58M1/4Ghq+ofIH0MvJlmcwhG47tv5mB9IWWaROu99oew5kzPfUmbwDWUUcDBLR6jreoWBlPJ7rxquB+bIdiqJdh8Bm+otHMCyVXAMke5dVmzZtCF3Wyps++aGaoGtAf+OfmLSa+t1cXgpur5BRyzm/ZOXmtZncJgLGlV3L8r8Ny/Ap5NKH99gece6GmsMzFLD2v2DXRT7EjHgaxZO9gM3/4L92IdtWUaA5xd0LEGzyXIu6pzsE0oruZWuDqFQR+wkbNs0avgAvAvCeXbudrzV85yg3u234evw+7xhGsZPNtuFL6f/UXKXZjU4LmfV5LdfOkGzolfn0N2h6m3v2d9hu6PqIU6hUGK58k3l344KTWDdjrBWW5w34q3h/80/6VwCavukT7gE87nraD8reW6sM6/LP3ADY5yZ2CL1PYjOwD/Oz6yTKDGTYVODYOR7A1nuV5Wn5r8U8dz+rE5GeclXE+jb6IPXwfYEuAsyu8v6MI37Lsc3++qG1uXsnVGuX6s2ej5u22BLYqqJYVB/QT8U1ePiP+OxdcWPRl71/bWqrYDvhq/noKvibCSapoIWS/ahqOwptJTGeXGYJ2oWRPg+rH+kd+QPRI03LBw5To1DMbR2ky7uvNOlW40FT7lKPsuNrEJrIPP+4Ltxm7ey53lb6XcVYoNKcuk7wNuwddZm+WnwAPYjlWe2tDe1HSHsU4Ng80Zfn5+Hn9Z8PFa8TjwoKPcdOCj2C7PWW5hVY3gTvx9JLsD78U/GWyOs1xVno//vkgxYdBocj1Eh2/BX6cwWAD80lm2F1snUJRNSRs++nqB5x7KS/g6pNbHpt96NhmZx6owCPhXSu6JDfl6hi2XYluPV2EPZ7lGCJ5P63tcXgc8HL++D1+N6ERanyXZFnUKA7A/jnfI8JMUs7dcD7Z0N2Wyzu0FnHc4y/HN3huF7RKd9XtYwJo7KqWsy/CG31cSjlkHrSxrB9uXc8SoWxg8BvzOWXYiaYuTmhmPrW/wbnCZ9wNHUqwE/gP4v4KO9wRw4xDnuMz5fG+t6X73FRXLs+EL2Db7A/0z8FrOcz4I3DTo/93ufG7K7s2lqVsYPIV/63CwSTGtThX9d/xbXkExAeRxP/BWQcd6i6EXDZ1e0PEbytzRaKAZznKPDPrv18kf7rcBzwz6fy84n1vL3ZLrFgavY++IXj3AKdhNnbK7bQ+2UcX12LRb7+9hKf6tzcHa2tOwTrhp+D/+Dayp4L25sny+yf9fRnGbj3wT//ZtYC+IqVhbfzrWSZm6Q3ODt1Y3VB/B6aQvqHoD64MZPHrgrdUWtX6kUHULA4BrE8uPxT5o9XL87/CfAr5PenXt58BvHeW2Bb6A1TquxoaffohVU0/Fv5T1C4nXN5R+4NdNvreU4pZkL8ffOz8b+AH2+7kB+4yKq4DPkm/u/pbOckP97bydtQO9ydCd3d5aY5mf2uVWx/HOZ7AOq88mPGcctrhkZnz+bay5n90OwKexWXRTSP9YtqVYh1FWM2YjbMx7Fqv/fhvTUHfFwugPHOcsYrHPcHv8FzVBaD72O88aZ98QW2B1LKsH4njs3XIXbIh3BsVPN2/mZWxYMKWp+GWGbhKVvcVbsar+sMcmj3VCCLc4P9SyLD8Ivmv/K+fxbnYe70stXPO7IYRxGcffMoRwVwvnCCGEp0MI62achxDCASGEZY7jPRdC2NRxPEIIx4cQFjqOeU8IYasmxzgqhDDfcYwQ7INsh7ueB5zHOTbjOKU/6thMAGvLfht4teoLiV6mebt7oI3wbzs2HaslZPEsqmnmYbLHvp+n9RGSe/F1Hl6Lb8frTbD9LIv0As33mfwJtluWxz9mfL9jawd1DYOAfUjHZfh2/mmnBdjQlaev4E8TjjsJOMxR7s2EYw52KfCOo9zNtDZ77lxnOe8uVqOxFYOelZiTKGbDmW87yjyJ7bRdhNT9N9uurmEA9k5zNtYxWFUgvIV1+M1zlveOd4P1J3g6Ep8CvpRw3IZlWO+2Z778FfhCoxnPqMdt2UVW04fv/hyNr+/rBYbfc+BKsu+ze8geMZjruBao4SYndQ6DhtnYh3aUvbnmIqwTs+wPARlsJbaFWKq7SeuA9KyFGMqN+GoV7ZitNxbb1KUow820XIjVVvP8LYayLra/QW10QhiAvTNeTHmTWhZg052/m/i8CxPKrsA3qShgMwhTJmOBvROm9Ln8ReLxG85ylkudqvwO2SEzEd8eC29gC7WyXErz2sOz+NbOvDPMMQaaiH9ItBSdEgYLsZuu1R1qPe7GFuf8JMdzr0koOx/fDQq2pXvW+vuBliVeC1h7OM/S45QJO97OtQVYP0bWFvaN/QGyLMX2l8zyOs07bP8TX7i+Sf5PtKpUp4QB2DvpA1gn1NewdQxFWYiFwMewIHiCfDv1/A6rxWSthuvHJiF5q/ELSZsP8Db5Nm1Nndp9Nf5Zd2AjMp4azmP4PuV5FL7djQK+oGt84tZQNZJr8d0Ty/HtR7Et7fvszlzqOOkoyyJszfwVwOHYh7TOwPcOMdgd2DviLdjNV0S/xFexm+l0hu49X4ZNWkn9tKG5+H/GvBN2ribtMwF/RNr6iSuwe+6LNP98gzuw/Qc9TcLFrLlYaCiv4m8yPYjVqgb+rh/FJiZ5vIr9XjxNhbrsuwlAVwidurU9YDvwTMR2nN0Baz9ujIXEUD31r2EJvwhbY3A/dtOlfghrljHYvPszsdl2DQ8Bf4/dwKkjJN49/sDewTw342C9pH2Izdukj0L0YetI5mAzQhtexkaP5uFfSehtJqR8luUobHbqwK3JFuP/1C2wv79nJ648v7+26fQwEJGCdFKfgYi0kcJARACFgYhECgMRARQGIhIpDEQEUBiISKQwEBFAYSAikcJARACFgYhECgMRARQGIhIpDEQEUBiISKQwEBFAYSAikcJARACFgYhECgMRARQGIhIpDEQEUBiISPT/9d+8SmcUuWQAAAAASUVORK5CYII=" alt="OWM 로고">
      <div class="brand-copy">
        <strong>Influencer Desk</strong>
        <span>옵티마웰니스 신사점</span>
      </div>
    </div>
    <nav class="nav">
      <button class="active" data-page="dashboard"><span class="icon">⌂</span><span class="label">대시보드</span></button>
      <button data-page="checkin"><span class="icon">✓</span><span class="label">방문 확인 · 응대</span></button>
      <button data-page="manage"><span class="icon">☷</span><span class="label">인플루언서 관리</span></button>
      <button data-page="logs"><span class="icon">↺</span><span class="label">방문 기록</span></button>
      <button data-page="backup"><span class="icon">⇩</span><span class="label">데이터 백업</span></button>
    </nav>
    <div class="side-note">
      <strong>운영 원칙</strong><br>
      검색 → 촬영 확인 → 기프트 수령 → 응대직원 기록까지 한 화면에서 처리합니다.
    </div>
  </aside>

  <main class="main">
    <header class="topbar">
      <div style="display:flex;align-items:center;gap:11px">
        <button class="btn btn-ghost mobile-menu" id="mobileMenu">☰</button>
        <div>
          <h1 id="pageTitle">대시보드</h1>
          <p id="pageDesc">오늘 방문 일정과 처리 현황을 한눈에 확인하세요.</p>
        </div>
      </div>
      <div class="top-actions">
        <button class="btn btn-ghost hide-mobile" id="sampleBtn">샘플 데이터</button>
        <button class="btn btn-pink" id="openAddBtn">＋ 인플루언서 추가</button>
      </div>
    </header>

    <section class="content">
      <div class="page active" id="page-dashboard">
        <div class="grid stats">
          <div class="stat dark">
            <div class="label">전체 인플루언서</div>
            <div class="value" id="statTotal">0</div>
            <div class="sub">통합 관리 중인 등록 건수</div>
          </div>
          <div class="stat pink">
            <div class="label">오늘 방문 예정</div>
            <div class="value" id="statToday">0</div>
            <div class="sub">오늘 날짜 기준 예정 건수</div>
          </div>
          <div class="stat">
            <div class="label">촬영 완료</div>
            <div class="value" id="statDone">0</div>
            <div class="sub">전체 누적 완료 건수</div>
          </div>
          <div class="stat">
            <div class="label">기프트 미수령</div>
            <div class="value" id="statGiftPending">0</div>
            <div class="sub">완료 전 확인이 필요한 건수</div>
          </div>
        </div>

        <div class="grid two-col" style="margin-top:18px">
          <div class="panel">
            <div class="panel-head">
              <div>
                <h2>오늘 방문 일정</h2>
                <p>방문 시간순으로 표시됩니다.</p>
              </div>
              <button class="btn btn-soft btn-sm" data-jump="checkin">방문 확인으로 이동</button>
            </div>
            <div id="todayList" class="mini-list"></div>
          </div>
          <div class="panel">
            <div class="panel-head">
              <div>
                <h2>최근 처리 기록</h2>
                <p>누가, 언제, 무엇을 처리했는지 남습니다.</p>
              </div>
            </div>
            <div id="recentLogs" class="log-list"></div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-head">
            <div>
              <h2>새로운 통합 응대 흐름</h2>
              <p>기존의 ‘시트 1 → 카톡 공지 → 시트 2’ 절차를 하나로 단순화합니다.</p>
            </div>
          </div>
          <div class="workflow">
            <div class="step"><div class="num">1</div><h4>통합 검색</h4><p>이름, 인스타 계정, 연락처 중 하나만 입력해 즉시 조회합니다.</p></div>
            <div class="step"><div class="num">2</div><h4>응대 정보 확인</h4><p>촬영 유형, 가이드, 기프트, 유료 금액, 비고를 한 화면에서 봅니다.</p></div>
            <div class="step"><div class="num">3</div><h4>처리 완료 체크</h4><p>촬영 완료와 기프트 수령 여부를 버튼으로 업데이트합니다.</p></div>
            <div class="step"><div class="num">4</div><h4>직원·이력 자동 기록</h4><p>응대직원과 처리 시간을 별도 방문 기록으로 계속 보존합니다.</p></div>
          </div>
        </div>
      </div>

      <div class="page" id="page-checkin">
        <div class="grid two-col">
          <div class="panel">
            <div class="panel-head">
              <div>
                <h2>인플루언서 통합 검색</h2>
                <p>이름 · 계정 주소 · 연락처를 검색하세요.</p>
              </div>
            </div>
            <div class="search-wrap">
              <span style="font-size:20px">⌕</span>
              <input id="checkinSearch" placeholder="예: @owm_demo, 방문자명, 010-0000-0000">
              <button class="btn btn-primary" id="checkinSearchBtn">검색</button>
            </div>
            <div class="search-tip">일부만 입력해도 조회됩니다. 검색 결과가 없으면 바로 신규 방문 기록을 추가할 수 있습니다.</div>
            <div class="result-area" id="checkinResults">
              <div class="empty"><div class="emoji">✨</div>검색어를 입력하면 방문 정보를 바로 확인할 수 있어요.</div>
            </div>
          </div>

          <div class="panel">
            <div class="panel-head">
              <div>
                <h2>오늘 빠른 확인</h2>
                <p>오늘 예정된 방문만 모아봅니다.</p>
              </div>
            </div>
            <div id="todayQuick" class="mini-list"></div>
          </div>
        </div>
      </div>

      <div class="page" id="page-manage">
        <div class="panel">
          <div class="panel-head">
            <div>
              <h2>인플루언서 관리</h2>
              <p>기존 시트의 열을 유지하면서 추가·수정·삭제할 수 있습니다.</p>
            </div>
            <button class="btn btn-primary" id="openAddBtn2">＋ 행 추가</button>
          </div>
          <div class="filters">
            <input id="manageSearch" placeholder="이름, 국가, 계정, 연락처 검색">
            <select id="statusFilter">
              <option value="">전체 상태</option>
              <option value="예정">예정</option>
              <option value="촬영중">촬영중</option>
              <option value="완료">완료</option>
              <option value="취소">취소</option>
            </select>
            <select id="countryFilter">
              <option value="">전체 국가</option>
            </select>
            <button class="btn btn-ghost" id="resetFilters">초기화</button>
          </div>
          <div class="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>협찬일</th><th>방문 시간</th><th>국가</th><th>계정주소</th><th>방문자명</th>
                  <th>연락처</th><th>촬영 유형</th><th>기프트</th><th>유료금액</th><th>비고</th>
                  <th>기프트 수령</th><th>응대직원</th><th>상태</th><th>관리</th>
                </tr>
              </thead>
              <tbody id="manageTableBody"></tbody>
            </table>
          </div>
        </div>
      </div>

      <div class="page" id="page-logs">
        <div class="panel">
          <div class="panel-head">
            <div>
              <h2>방문·처리 기록</h2>
              <p>인플루언서 정보가 수정되더라도 방문 이력은 별도로 남습니다.</p>
            </div>
            <button class="btn btn-danger btn-sm" id="clearLogsBtn">기록 전체 삭제</button>
          </div>
          <div class="filters">
            <input id="logSearch" placeholder="방문자명, 직원명, 처리 내용 검색">
          </div>
          <div id="fullLogList" class="log-list"></div>
        </div>
      </div>

      <div class="page" id="page-backup">
        <div class="notice">
          현재 프로토타입은 이 브라우저의 저장공간(localStorage)에 보관됩니다. 같은 컴퓨터·같은 브라우저에서는 새로고침 후에도 유지되지만, 여러 직원이 여러 컴퓨터에서 함께 사용하려면 다음 단계에서 Supabase 또는 Firebase 같은 온라인 데이터베이스 연결이 필요합니다.
        </div>
        <div class="grid two-col">
          <div class="panel">
            <div class="panel-head">
              <div>
                <h2>백업 · 내보내기</h2>
                <p>정기적으로 파일을 내려받아 보관할 수 있습니다.</p>
              </div>
            </div>
            <div style="display:flex;gap:10px;flex-wrap:wrap">
              <button class="btn btn-primary" id="exportJsonBtn">JSON 전체 백업</button>
              <button class="btn btn-ghost" id="exportCsvBtn">CSV로 내보내기</button>
            </div>
          </div>
          <div class="panel">
            <div class="panel-head">
              <div>
                <h2>가져오기</h2>
                <p>이 사이트에서 만든 JSON 백업 또는 구글시트에서 저장한 CSV를 불러옵니다.</p>
              </div>
            </div>
            <div style="display:flex;gap:10px;flex-wrap:wrap">
              <label class="btn btn-soft" for="importJsonInput">JSON 불러오기</label>
              <input id="importJsonInput" type="file" accept=".json" hidden>
              <label class="btn btn-ghost" for="importCsvInput">CSV 불러오기</label>
              <input id="importCsvInput" type="file" accept=".csv,text/csv" hidden>
            </div>
          </div>
        </div>
        <div class="panel">
          <div class="panel-head">
            <div>
              <h2>온라인 운영 전환 체크리스트</h2>
              <p>실제 약국 운영에 적용할 때 필요한 항목입니다.</p>
            </div>
          </div>
          <div class="workflow">
            <div class="step"><div class="num">1</div><h4>직원 로그인</h4><p>관리자와 응대직원의 권한을 나눕니다.</p></div>
            <div class="step"><div class="num">2</div><h4>클라우드 DB</h4><p>모든 컴퓨터에서 같은 최신 데이터를 봅니다.</p></div>
            <div class="step"><div class="num">3</div><h4>변경 이력</h4><p>삭제·수정한 직원과 시간을 자동 기록합니다.</p></div>
            <div class="step"><div class="num">4</div><h4>개인정보 보호</h4><p>연락처 접근 권한, 보관 기간, 백업 정책을 설정합니다.</p></div>
          </div>
        </div>
      </div>
    </section>
  </main>
</div>

<div class="modal-backdrop" id="recordModal">
  <div class="modal">
    <div class="modal-head">
      <h2 id="modalTitle">인플루언서 추가</h2>
      <button class="close" data-close="recordModal">×</button>
    </div>
    <form id="recordForm">
      <input type="hidden" id="recordId">
      <div class="form-grid">
        <div class="field"><label>협찬일 *</label><input type="date" id="sponsorDate" required></div>
        <div class="field"><label>방문 시간</label><input type="time" id="visitTime"></div>
        <div class="field"><label>국가</label><input id="country" placeholder="예: 영어권, 중국, 일본"></div>
        <div class="field"><label>방문자명 *</label><input id="visitorName" required placeholder="이름 또는 활동명"></div>
        <div class="field full"><label>계정주소</label><input id="accountUrl" placeholder="인스타그램, 틱톡, 샤오홍슈 등 URL"></div>
        <div class="field"><label>연락처</label><input id="contact" placeholder="010-0000-0000"></div>
        <div class="field"><label>촬영 유형 선택 / 가이드</label><input id="shootType" placeholder="예: 에피미러 X OWM"></div>
        <div class="field"><label>기프트</label><input id="gift" placeholder="예: REJU-ECTO, JUVE-ECTO"></div>
        <div class="field"><label>유료금액</label><input type="number" min="0" step="1000" id="paidAmount" placeholder="0"></div>
        <div class="field"><label>응대직원</label><input id="staff" placeholder="직원 이름"></div>
        <div class="field"><label>상태</label>
          <select id="status">
            <option value="예정">예정</option>
            <option value="촬영중">촬영중</option>
            <option value="완료">완료</option>
            <option value="취소">취소</option>
          </select>
        </div>
        <div class="field">
          <label>기프트 수령</label>
          <div class="checkline"><input type="checkbox" id="giftReceived"><span>수령 완료로 체크</span></div>
        </div>
        <div class="field full"><label>비고</label><textarea id="notes" placeholder="약국 및 피부과 협업 경험, 별도 요청, 주의사항 등"></textarea></div>
      </div>
      <div class="modal-actions">
        <button type="button" class="btn btn-ghost" data-close="recordModal">취소</button>
        <button type="submit" class="btn btn-pink">저장</button>
      </div>
    </form>
  </div>
</div>

<div class="modal-backdrop" id="completeModal">
  <div class="modal" style="width:min(560px,100%)">
    <div class="modal-head">
      <h2>촬영 완료 처리</h2>
      <button class="close" data-close="completeModal">×</button>
    </div>
    <form id="completeForm">
      <input type="hidden" id="completeId">
      <div class="form-grid">
        <div class="field full"><label>응대직원 *</label><input id="completeStaff" required placeholder="오늘 응대한 직원 이름"></div>
        <div class="field full">
          <label>기프트 수령</label>
          <div class="checkline"><input type="checkbox" id="completeGift" checked><span>기프트 수령 완료</span></div>
        </div>
        <div class="field full"><label>처리 메모</label><textarea id="completeNote" placeholder="추가 요청이나 전달사항이 있으면 남겨주세요."></textarea></div>
      </div>
      <div class="modal-actions">
        <button type="button" class="btn btn-ghost" data-close="completeModal">취소</button>
        <button type="submit" class="btn btn-pink">완료 처리</button>
      </div>
    </form>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const STORAGE_KEY='owm_influencer_records_v1';
const LOG_KEY='owm_influencer_logs_v1';

let records = safeParse(localStorage.getItem(STORAGE_KEY), []);
let logs = safeParse(localStorage.getItem(LOG_KEY), []);

const pageMeta={
  dashboard:['대시보드','오늘 방문 일정과 처리 현황을 한눈에 확인하세요.'],
  checkin:['방문 확인 · 응대','검색부터 촬영 완료, 기프트 수령, 직원 기록까지 한 번에 처리합니다.'],
  manage:['인플루언서 관리','모든 인플루언서 정보를 한 시트처럼 추가·수정·관리합니다.'],
  logs:['방문 기록','방문과 처리 이력을 시간순으로 확인합니다.'],
  backup:['데이터 백업','현재 데이터를 내보내거나 기존 시트 데이터를 가져옵니다.']
};

function safeParse(value,fallback){
  try{return value?JSON.parse(value):fallback}catch(e){return fallback}
}
function uid(){
  return (crypto.randomUUID?crypto.randomUUID():'id-'+Date.now()+'-'+Math.random().toString(16).slice(2));
}
function todayISO(){
  const d=new Date();
  const offset=d.getTimezoneOffset();
  return new Date(d.getTime()-offset*60*1000).toISOString().slice(0,10);
}
function nowText(){
  return new Intl.DateTimeFormat('ko-KR',{year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit'}).format(new Date());
}
function saveAll(){
  localStorage.setItem(STORAGE_KEY,JSON.stringify(records));
  localStorage.setItem(LOG_KEY,JSON.stringify(logs));
  renderAll();
}
function formatMoney(v){
  const n=Number(v||0);
  return n?new Intl.NumberFormat('ko-KR').format(n)+'원':'-';
}
function escapeHtml(v=''){
  return String(v).replace(/[&<>"']/g,s=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[s]));
}
function statusClass(s){
  return s==='완료'?'done':s==='촬영중'?'progress':s==='취소'?'cancel':'upcoming';
}
function initials(name=''){
  return name.trim().slice(0,2)||'OW';
}
function addLog(record,type,staff,note=''){
  logs.unshift({
    id:uid(),
    recordId:record.id,
    visitorName:record.visitorName||'이름 없음',
    accountUrl:record.accountUrl||'',
    type,
    staff:staff||record.staff||'미입력',
    note,
    at:new Date().toISOString()
  });
}
function toast(msg){
  const el=document.getElementById('toast');
  el.textContent=msg;
  el.classList.add('show');
  clearTimeout(window.__toastTimer);
  window.__toastTimer=setTimeout(()=>el.classList.remove('show'),2200);
}
function setPage(page){
  document.querySelectorAll('.page').forEach(el=>el.classList.toggle('active',el.id==='page-'+page));
  document.querySelectorAll('.nav button').forEach(el=>el.classList.toggle('active',el.dataset.page===page));
  document.getElementById('pageTitle').textContent=pageMeta[page][0];
  document.getElementById('pageDesc').textContent=pageMeta[page][1];
  document.getElementById('sidebar').classList.remove('open');
  if(page==='checkin')setTimeout(()=>document.getElementById('checkinSearch').focus(),50);
}
document.querySelectorAll('.nav button').forEach(btn=>btn.addEventListener('click',()=>setPage(btn.dataset.page)));
document.querySelectorAll('[data-jump]').forEach(btn=>btn.addEventListener('click',()=>setPage(btn.dataset.jump)));
document.getElementById('mobileMenu').addEventListener('click',()=>document.getElementById('sidebar').classList.toggle('open'));

function renderStats(){
  const today=todayISO();
  document.getElementById('statTotal').textContent=records.length;
  document.getElementById('statToday').textContent=records.filter(r=>r.sponsorDate===today && r.status!=='취소').length;
  document.getElementById('statDone').textContent=records.filter(r=>r.status==='완료').length;
  document.getElementById('statGiftPending').textContent=records.filter(r=>r.status!=='취소' && !r.giftReceived).length;
}
function todayRecords(){
  return records.filter(r=>r.sponsorDate===todayISO()&&r.status!=='취소')
    .sort((a,b)=>(a.visitTime||'99:99').localeCompare(b.visitTime||'99:99'));
}
function renderToday(){
  const list=todayRecords();
  const html=list.length?list.map(r=>`
    <div class="mini-row">
      <div>
        <strong>${escapeHtml(r.visitTime||'시간 미정')} · ${escapeHtml(r.visitorName)}</strong>
        <span>${escapeHtml(r.country||'국가 미입력')} · ${escapeHtml(r.shootType||'촬영 유형 미입력')}</span>
      </div>
      <span class="badge ${statusClass(r.status)}">${escapeHtml(r.status)}</span>
    </div>`).join(''):`<div class="empty"><div class="emoji">🌿</div>오늘 예정된 방문이 없습니다.</div>`;
  document.getElementById('todayList').innerHTML=html;
  document.getElementById('todayQuick').innerHTML=html;
}
function logHtml(log){
  const d=new Date(log.at);
  const date=d.toLocaleDateString('ko-KR');
  const time=d.toLocaleTimeString('ko-KR',{hour:'2-digit',minute:'2-digit'});
  const icon=log.type.includes('완료')?'✓':log.type.includes('수정')?'✎':log.type.includes('삭제')?'⌫':'＋';
  return `<div class="log-item">
    <div class="log-icon">${icon}</div>
    <div class="log-main">
      <strong>${escapeHtml(log.visitorName)} · ${escapeHtml(log.type)}</strong>
      <span>응대직원 ${escapeHtml(log.staff||'미입력')}${log.note?' · '+escapeHtml(log.note):''}</span>
    </div>
    <div class="log-time">${date}<br>${time}</div>
  </div>`;
}
function renderLogs(){
  const recent=logs.slice(0,4);
  document.getElementById('recentLogs').innerHTML=recent.length?recent.map(logHtml).join(''):`<div class="empty">아직 처리 기록이 없습니다.</div>`;
  const q=document.getElementById('logSearch').value.trim().toLowerCase();
  const filtered=logs.filter(l=>[l.visitorName,l.staff,l.type,l.note].join(' ').toLowerCase().includes(q));
  document.getElementById('fullLogList').innerHTML=filtered.length?filtered.map(logHtml).join(''):`<div class="empty">조건에 맞는 기록이 없습니다.</div>`;
}
function renderCountries(){
  const select=document.getElementById('countryFilter');
  const current=select.value;
  const countries=[...new Set(records.map(r=>r.country).filter(Boolean))].sort();
  select.innerHTML='<option value="">전체 국가</option>'+countries.map(c=>`<option value="${escapeHtml(c)}">${escapeHtml(c)}</option>`).join('');
  if(countries.includes(current))select.value=current;
}
function renderManage(){
  const q=document.getElementById('manageSearch').value.trim().toLowerCase();
  const status=document.getElementById('statusFilter').value;
  const country=document.getElementById('countryFilter').value;
  const rows=records.filter(r=>{
    const text=[r.visitorName,r.country,r.accountUrl,r.contact,r.shootType,r.gift,r.staff].join(' ').toLowerCase();
    return (!q||text.includes(q))&&(!status||r.status===status)&&(!country||r.country===country);
  }).sort((a,b)=>(b.sponsorDate||'').localeCompare(a.sponsorDate||'')||(a.visitTime||'').localeCompare(b.visitTime||''));
  document.getElementById('manageTableBody').innerHTML=rows.length?rows.map(r=>`
    <tr>
      <td>${escapeHtml(r.sponsorDate||'-')}</td>
      <td>${escapeHtml(r.visitTime||'-')}</td>
      <td>${escapeHtml(r.country||'-')}</td>
      <td><a class="account" href="${/^https?:\/\//.test(r.accountUrl||'')?escapeHtml(r.accountUrl):'#'}" target="_blank">${escapeHtml(r.accountUrl||'-')}</a></td>
      <td><strong>${escapeHtml(r.visitorName||'-')}</strong></td>
      <td>${escapeHtml(r.contact||'-')}</td>
      <td>${escapeHtml(r.shootType||'-')}</td>
      <td>${escapeHtml(r.gift||'-')}</td>
      <td>${formatMoney(r.paidAmount)}</td>
      <td><span title="${escapeHtml(r.notes||'')}">${escapeHtml((r.notes||'-').slice(0,24))}${(r.notes||'').length>24?'…':''}</span></td>
      <td>${r.giftReceived?'⭕':'—'}</td>
      <td>${escapeHtml(r.staff||'-')}</td>
      <td><span class="badge ${statusClass(r.status)}">${escapeHtml(r.status||'예정')}</span></td>
      <td><div class="row-actions">
        <button class="btn btn-ghost btn-sm" onclick="editRecord('${r.id}')">수정</button>
        <button class="btn btn-danger btn-sm" onclick="deleteRecord('${r.id}')">삭제</button>
      </div></td>
    </tr>`).join(''):`<tr><td colspan="14" style="text-align:center;padding:30px;color:#777">등록된 정보가 없습니다.</td></tr>`;
}
function renderAll(){
  renderStats();
  renderToday();
  renderCountries();
  renderManage();
  renderLogs();
}

function openRecordModal(record=null){
  document.getElementById('modalTitle').textContent=record?'인플루언서 수정':'인플루언서 추가';
  document.getElementById('recordForm').reset();
  document.getElementById('recordId').value=record?.id||'';
  document.getElementById('sponsorDate').value=record?.sponsorDate||todayISO();
  document.getElementById('visitTime').value=record?.visitTime||'';
  document.getElementById('country').value=record?.country||'';
  document.getElementById('visitorName').value=record?.visitorName||'';
  document.getElementById('accountUrl').value=record?.accountUrl||'';
  document.getElementById('contact').value=record?.contact||'';
  document.getElementById('shootType').value=record?.shootType||'';
  document.getElementById('gift').value=record?.gift||'';
  document.getElementById('paidAmount').value=record?.paidAmount||'';
  document.getElementById('staff').value=record?.staff||'';
  document.getElementById('status').value=record?.status||'예정';
  document.getElementById('giftReceived').checked=!!record?.giftReceived;
  document.getElementById('notes').value=record?.notes||'';
  document.getElementById('recordModal').classList.add('open');
}
window.editRecord=id=>openRecordModal(records.find(r=>r.id===id));
window.deleteRecord=id=>{
  const r=records.find(x=>x.id===id);
  if(!r||!confirm(`${r.visitorName} 정보를 삭제할까요?`))return;
  records=records.filter(x=>x.id!==id);
  addLog(r,'정보 삭제',r.staff||'관리자');
  saveAll();
  toast('삭제했습니다.');
};

document.getElementById('recordForm').addEventListener('submit',e=>{
  e.preventDefault();
  const id=document.getElementById('recordId').value;
  const old=records.find(r=>r.id===id);
  const data={
    id:id||uid(),
    sponsorDate:document.getElementById('sponsorDate').value,
    visitTime:document.getElementById('visitTime').value,
    country:document.getElementById('country').value.trim(),
    visitorName:document.getElementById('visitorName').value.trim(),
    accountUrl:document.getElementById('accountUrl').value.trim(),
    contact:document.getElementById('contact').value.trim(),
    shootType:document.getElementById('shootType').value.trim(),
    gift:document.getElementById('gift').value.trim(),
    paidAmount:Number(document.getElementById('paidAmount').value||0),
    staff:document.getElementById('staff').value.trim(),
    status:document.getElementById('status').value,
    giftReceived:document.getElementById('giftReceived').checked,
    notes:document.getElementById('notes').value.trim(),
    updatedAt:new Date().toISOString(),
    createdAt:old?.createdAt||new Date().toISOString()
  };
  if(old){
    records=records.map(r=>r.id===id?data:r);
    addLog(data,'정보 수정',data.staff||'관리자');
  }else{
    records.push(data);
    addLog(data,'신규 등록',data.staff||'관리자');
  }
  document.getElementById('recordModal').classList.remove('open');
  saveAll();
  toast(old?'수정했습니다.':'새 인플루언서를 등록했습니다.');
});

function matchCard(r){
  return `<div class="match-card">
    <div class="match-top">
      <div class="identity">
        <div class="avatar">${escapeHtml(initials(r.visitorName))}</div>
        <div style="min-width:0">
          <h3>${escapeHtml(r.visitorName)} <span class="badge ${statusClass(r.status)}">${escapeHtml(r.status)}</span></h3>
          <p>${escapeHtml(r.accountUrl||'계정주소 미입력')}</p>
        </div>
      </div>
      <span class="pill">${escapeHtml(r.country||'국가 미입력')}</span>
    </div>
    <div class="detail-grid">
      <div class="detail"><span>협찬일 · 시간</span><strong>${escapeHtml(r.sponsorDate||'-')} ${escapeHtml(r.visitTime||'')}</strong></div>
      <div class="detail"><span>촬영 유형</span><strong>${escapeHtml(r.shootType||'-')}</strong></div>
      <div class="detail"><span>기프트</span><strong>${escapeHtml(r.gift||'-')}</strong></div>
      <div class="detail"><span>유료금액</span><strong>${formatMoney(r.paidAmount)}</strong></div>
      <div class="detail"><span>연락처</span><strong>${escapeHtml(r.contact||'-')}</strong></div>
      <div class="detail"><span>기프트 수령</span><strong>${r.giftReceived?'완료 ⭕':'미수령'}</strong></div>
    </div>
    ${r.notes?`<div class="notice" style="margin:14px 0 0"><strong>비고</strong><br>${escapeHtml(r.notes)}</div>`:''}
    <div class="card-actions">
      <button class="btn btn-pink" onclick="openComplete('${r.id}')">✓ 촬영 완료 처리</button>
      <button class="btn btn-ghost" onclick="startShoot('${r.id}')">촬영 시작</button>
      <button class="btn btn-ghost" onclick="editRecord('${r.id}')">정보 수정</button>
    </div>
  </div>`;
}
function runCheckinSearch(){
  const q=document.getElementById('checkinSearch').value.trim().toLowerCase();
  const area=document.getElementById('checkinResults');
  if(!q){
    area.innerHTML='<div class="empty"><div class="emoji">✨</div>검색어를 입력하면 방문 정보를 바로 확인할 수 있어요.</div>';
    return;
  }
  const matches=records.filter(r=>[r.visitorName,r.accountUrl,r.contact,r.country].join(' ').toLowerCase().includes(q));
  if(matches.length){
    area.innerHTML=matches.map(matchCard).join('');
  }else{
    area.innerHTML=`<div class="empty">
      <div class="emoji">🔎</div>
      <strong>등록된 인플루언서를 찾지 못했습니다.</strong>
      <p style="margin:8px 0 15px">카톡이나 별도 공지를 다시 찾지 않고, 여기에서 바로 신규 방문 건을 추가하세요.</p>
      <button class="btn btn-pink" id="quickAddFromSearch">＋ 신규 방문 기록 추가</button>
    </div>`;
    document.getElementById('quickAddFromSearch').addEventListener('click',()=>{
      openRecordModal();
      const raw=document.getElementById('checkinSearch').value.trim();
      if(raw.includes('@')||raw.includes('http'))document.getElementById('accountUrl').value=raw;
      else document.getElementById('visitorName').value=raw;
    });
  }
}
document.getElementById('checkinSearchBtn').addEventListener('click',runCheckinSearch);
document.getElementById('checkinSearch').addEventListener('keydown',e=>{if(e.key==='Enter')runCheckinSearch()});

window.startShoot=id=>{
  const r=records.find(x=>x.id===id); if(!r)return;
  r.status='촬영중';r.updatedAt=new Date().toISOString();
  addLog(r,'촬영 시작',r.staff||'미입력');
  saveAll();
  runCheckinSearch();
  toast('촬영중으로 변경했습니다.');
};
window.openComplete=id=>{
  const r=records.find(x=>x.id===id); if(!r)return;
  document.getElementById('completeForm').reset();
  document.getElementById('completeId').value=id;
  document.getElementById('completeStaff').value=r.staff||'';
  document.getElementById('completeGift').checked=true;
  document.getElementById('completeModal').classList.add('open');
};
document.getElementById('completeForm').addEventListener('submit',e=>{
  e.preventDefault();
  const id=document.getElementById('completeId').value;
  const r=records.find(x=>x.id===id); if(!r)return;
  r.status='완료';
  r.giftReceived=document.getElementById('completeGift').checked;
  r.staff=document.getElementById('completeStaff').value.trim();
  r.updatedAt=new Date().toISOString();
  addLog(r,'촬영 완료',r.staff,document.getElementById('completeNote').value.trim());
  document.getElementById('completeModal').classList.remove('open');
  saveAll();
  runCheckinSearch();
  toast('촬영 완료와 방문 기록을 저장했습니다.');
});

document.querySelectorAll('[data-close]').forEach(btn=>btn.addEventListener('click',()=>document.getElementById(btn.dataset.close).classList.remove('open')));
document.querySelectorAll('.modal-backdrop').forEach(el=>el.addEventListener('click',e=>{if(e.target===el)el.classList.remove('open')}));

['openAddBtn','openAddBtn2'].forEach(id=>document.getElementById(id).addEventListener('click',()=>openRecordModal()));
document.getElementById('manageSearch').addEventListener('input',renderManage);
document.getElementById('statusFilter').addEventListener('change',renderManage);
document.getElementById('countryFilter').addEventListener('change',renderManage);
document.getElementById('resetFilters').addEventListener('click',()=>{
  document.getElementById('manageSearch').value='';
  document.getElementById('statusFilter').value='';
  document.getElementById('countryFilter').value='';
  renderManage();
});
document.getElementById('logSearch').addEventListener('input',renderLogs);
document.getElementById('clearLogsBtn').addEventListener('click',()=>{
  if(!logs.length||!confirm('방문 기록을 모두 삭제할까요?'))return;
  logs=[];saveAll();toast('방문 기록을 삭제했습니다.');
});

function download(filename,text,type='application/octet-stream'){
  const blob=new Blob([text],{type});
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');a.href=url;a.download=filename;a.click();
  setTimeout(()=>URL.revokeObjectURL(url),1000);
}
document.getElementById('exportJsonBtn').addEventListener('click',()=>{
  download(`OWM_인플루언서_백업_${todayISO()}.json`,JSON.stringify({records,logs,exportedAt:new Date().toISOString()},null,2),'application/json');
});
const csvHeaders=['협찬일','방문 시간','국가','계정주소','방문자명','연락처','촬영 유형','기프트','유료금액','비고','기프트 수령','응대직원','상태'];
function csvEscape(v){
  const s=String(v??'');
  return /[",\n]/.test(s)?`"${s.replace(/"/g,'""')}"`:s;
}
document.getElementById('exportCsvBtn').addEventListener('click',()=>{
  const rows=records.map(r=>[
    r.sponsorDate,r.visitTime,r.country,r.accountUrl,r.visitorName,r.contact,r.shootType,r.gift,
    r.paidAmount,r.notes,r.giftReceived?'TRUE':'FALSE',r.staff,r.status
  ]);
  const csv='\uFEFF'+[csvHeaders,...rows].map(row=>row.map(csvEscape).join(',')).join('\n');
  download(`OWM_인플루언서_리스트_${todayISO()}.csv`,csv,'text/csv;charset=utf-8');
});
document.getElementById('importJsonInput').addEventListener('change',async e=>{
  const file=e.target.files[0];if(!file)return;
  try{
    const data=JSON.parse(await file.text());
    if(!Array.isArray(data.records))throw new Error('형식 오류');
    if(!confirm(`기존 데이터에 ${data.records.length}건을 덮어쓸까요?`))return;
    records=data.records;logs=Array.isArray(data.logs)?data.logs:[];
    saveAll();toast('JSON 백업을 불러왔습니다.');
  }catch(err){alert('올바른 OWM JSON 백업 파일이 아닙니다.')}
  e.target.value='';
});
function parseCSV(text){
  const rows=[];let row=[],cell='',q=false;
  for(let i=0;i<text.length;i++){
    const c=text[i],n=text[i+1];
    if(q){
      if(c==='"'&&n==='"'){cell+='"';i++}
      else if(c==='"'){q=false}
      else cell+=c;
    }else{
      if(c==='"')q=true;
      else if(c===','){row.push(cell);cell=''}
      else if(c==='\n'){row.push(cell);rows.push(row);row=[];cell=''}
      else if(c!=='\r')cell+=c;
    }
  }
  if(cell.length||row.length){row.push(cell);rows.push(row)}
  return rows;
}
function normalizeHeader(h){
  return h.replace(/\s+/g,'').replace(/[()]/g,'').toLowerCase();
}
document.getElementById('importCsvInput').addEventListener('change',async e=>{
  const file=e.target.files[0];if(!file)return;
  try{
    const text=(await file.text()).replace(/^\uFEFF/,'');
    const rows=parseCSV(text);
    if(rows.length<2)throw new Error('데이터 없음');
    const headers=rows[0].map(normalizeHeader);
    const find=(...cands)=>headers.findIndex(h=>cands.map(normalizeHeader).includes(h));
    const idx={
      sponsorDate:find('협찬일','날짜','방문일'),
      visitTime:find('방문시간','시간'),
      country:find('국가'),
      accountUrl:find('계정주소','계정','sns','인스타그램'),
      visitorName:find('방문자명','이름','성명'),
      contact:find('연락처','전화번호'),
      shootType:find('촬영유형','촬영유형선택/가이드','가이드'),
      gift:find('기프트','선물'),
      paidAmount:find('유료금액','금액'),
      notes:find('비고','메모'),
      giftReceived:find('기프트수령','수령'),
      staff:find('응대직원','직원'),
      status:find('상태')
    };
    const imported=rows.slice(1).filter(row=>row.some(Boolean)).map(row=>({
      id:uid(),
      sponsorDate:idx.sponsorDate>=0?row[idx.sponsorDate]:'',
      visitTime:idx.visitTime>=0?row[idx.visitTime]:'',
      country:idx.country>=0?row[idx.country]:'',
      accountUrl:idx.accountUrl>=0?row[idx.accountUrl]:'',
      visitorName:idx.visitorName>=0?row[idx.visitorName]:'이름 미입력',
      contact:idx.contact>=0?row[idx.contact]:'',
      shootType:idx.shootType>=0?row[idx.shootType]:'',
      gift:idx.gift>=0?row[idx.gift]:'',
      paidAmount:idx.paidAmount>=0?Number(String(row[idx.paidAmount]).replace(/[^\d.-]/g,''))||0:0,
      notes:idx.notes>=0?row[idx.notes]:'',
      giftReceived:idx.giftReceived>=0?/true|o|⭕|완료|수령/i.test(row[idx.giftReceived]):false,
      staff:idx.staff>=0?row[idx.staff]:'',
      status:idx.status>=0&&row[idx.status]?row[idx.status]:'예정',
      createdAt:new Date().toISOString(),updatedAt:new Date().toISOString()
    }));
    if(!confirm(`${imported.length}건을 기존 데이터에 추가할까요?`))return;
    records.push(...imported);
    saveAll();toast(`${imported.length}건을 가져왔습니다.`);
  }catch(err){alert('CSV 파일을 읽지 못했습니다. 첫 행에 열 제목이 있는지 확인해주세요.')}
  e.target.value='';
});

document.getElementById('sampleBtn').addEventListener('click',()=>{
  if(records.length&&!confirm('현재 데이터가 있습니다. 샘플 3건을 추가할까요?'))return;
  const t=todayISO();
  const sample=[
    {visitorName:'OWM Demo A',country:'영어권',accountUrl:'https://instagram.com/owm_demo_a',contact:'010-0000-0001',shootType:'에피미러 X OWM',gift:'REJU-ECTO · JUVE-ECTO',paidAmount:450000,notes:'약국 및 피부과 협업 경험이 있는 예시 계정입니다.',giftReceived:false,staff:'',status:'예정',sponsorDate:t,visitTime:'14:30'},
    {visitorName:'OWM Demo B',country:'중국',accountUrl:'https://instagram.com/owm_demo_b',contact:'010-0000-0002',shootType:'레비온 X OWM 캠페인',gift:'레비온 PDRN 크림',paidAmount:300000,notes:'샘플 데이터입니다.',giftReceived:true,staff:'희선',status:'완료',sponsorDate:t,visitTime:'16:00'},
    {visitorName:'OWM Demo C',country:'일본',accountUrl:'https://instagram.com/owm_demo_c',contact:'010-0000-0003',shootType:'에피미러 X OWM',gift:'JUVE-ECTO',paidAmount:0,notes:'별도 요청 없음.',giftReceived:false,staff:'',status:'예정',sponsorDate:t,visitTime:'17:30'}
  ].map(x=>({...x,id:uid(),createdAt:new Date().toISOString(),updatedAt:new Date().toISOString()}));
  records.push(...sample);
  addLog(sample[1],'촬영 완료','희선','샘플 기록');
  saveAll();toast('샘플 데이터를 추가했습니다.');
});

renderAll();
</script>
</body>
</html>
