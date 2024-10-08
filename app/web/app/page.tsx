"use client";
import { MdPreview } from "md-editor-rt";
import "md-editor-rt/lib/preview.css";
import { useState } from "react";

const markdownContent = `


# 台灣市場面臨的多重挑戰及應對策略

## **股市波動與社會議題**
根據提供的新聞內容，可以看出台灣市場受到了多重因素的影響，從股市波動到家暴問題都反映出社會的多元議題。首先，台灣股市的高低震盪以及極端的漲跌幅度顯示市場的不穩定性，可能受到國際經濟和政治環境的波動影響。這對台灣的投資者和經濟體系都具有重要的影響，需要謹慎應對。

## **家庭暴力議題的關注**
另一方面，近期一起關於家庭暴力的案件受到廣泛關注，法院支持受害者的離婚申請，這提醒著社會家庭暴力問題的嚴重性。這也引起社會更多對家庭暴力議題的關注，呼籲更多的支持和資源投入到預防和處理家庭暴力的工作上。這不僅是一個家庭的問題，更關乎整個社會的安全和和諧。

## **製造業挑戰和全球經濟影響**
此外，製造業景氣指數下滑和外銷新訂單縮減，顯示出台灣的製造業面臨著挑戰。全球經濟下滑和貿易壓力對製造業造成了影響，這對台灣的經濟增長和出口產業都帶來了影響。加上歐洲央行和美國聯準會等央行的降息政策，全球市場的不確定性進一步加劇，對台灣的金融市場和投資環境也帶來了波動。

## **人工智能與科技創新**
同時，人工智能市場持續快速發展，可能對台灣企業和經濟運作方式帶來前所未有的變革和挑戰。台灣應當加強對新興科技的研究和應用，以提高產業競爭力。中國央行的降準降息舉措也可能對全球市場造成影響，特別對銅價和房地產市場有潛在的影響。

## **結語**
綜上所述，台灣面臨著來自國際和國內多方面的挑戰，從金融市場的波動到社會議題的嚴峻情況。台灣應該保持警醒，加強應對這些挑戰，同時積極面對變革和創新，以促進經濟的穩健增長與社會的進步。

`;
export default function MarkdownPage() {
  const [id] = useState("preview-only");

  return (
    <div className="container mx-auto p-5">
      <h1 className="text-4xl font-extrabold mb-6 text-center ">
        每日新聞摘要
      </h1>
      <div className="shadow-lg rounded-lg p-8 bg-white">
        <MdPreview
          editorId={id}
          modelValue={markdownContent}
          language="en-US"
        />
      </div>
    </div>
  );
}
