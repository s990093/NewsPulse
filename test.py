from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 定義文章內容
text = (
    "經濟類台灣市場面臨的多重挑戰及應對策略 "
    "台灣面臨挑戰 國際 國內 金融市場 波動 社會議題 嚴峻 "
    "台灣應該保持警醒 加強應對 挑戰 促進經濟穩健增長 "
    "股市波動 社會議題 家庭暴力 製造業挑戰 全球經濟影響 "
    "人工智能 科技創新 產業競爭力 降息政策 全球市場不確定性 "
)

# 生成文字雲
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color="white",
    colormap="viridis",
    font_path=None,  # 可以指定中文字型，例如 "path/to/font.ttf"
    max_words=100
).generate(text)

# 顯示文字雲
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("台灣市場挑戰文字雲", fontsize=20)
plt.show()