async function decodeUrls(articles) {
    // 構造 `articles_reqs` 數據
    const articlesReqs = articles.map(art => [
        "Fbv4je",
        `["garturlreq",[["X","X",["X","X"],null,null,1,1,"US:en",null,1,null,null,null,null,null,0,1],"X","X",1,[1,1,1],1,1,null,0,0,null,0],"${art.gn_art_id}",${art.timestamp},"${art.signature}"]`
    ]);

    // 將數據轉換為符合要求的格式
    const payload = `f.req=${encodeURIComponent(JSON.stringify([articlesReqs]))}`;

    const headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    };

    // 發送 POST 請求
    const response = await fetch("https://news.google.com/_/DotsSplashUi/data/batchexecute", {
        method: "POST",
        headers: headers,
        body: payload
    });

    if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
    }

    const responseText = await response.text();
    const splitResponse = responseText.split("\n\n");

    // 解碼並返回結果
    const parsedResponse = JSON.parse(splitResponse[1]);
    return parsedResponse.slice(0, -2).map(res => JSON.parse(res[2])[1]);
}
