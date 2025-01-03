"use client";
import { useState } from "react";
import { FaPlay, FaStop, FaVolumeUp, FaPlayCircle } from "react-icons/fa";
import { articles } from "./articles";
import { motion } from "framer-motion";
import { Bar } from "react-chartjs-2";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default function NewsCards() {
  const [playing, setPlaying] = useState(null);

  // 假數據：各類新聞的數量
  const categories = ["政治", "經濟", "科技", "娛樂", "體育"];
  const fakeData = [12, 8, 15, 5, 10]; // 假設這是每個分類的新聞數量
  const totalNews = 409;

  const speak = (text, index) => {
    if (playing !== null) {
      speechSynthesis.cancel();
      setPlaying(null);
    }
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = "zh-TW";
    utterance.onend = () => setPlaying(null);
    speechSynthesis.speak(utterance);
    setPlaying(index);
  };

  const stopSpeaking = () => {
    speechSynthesis.cancel();
    setPlaying(null);
  };

  const speakAll = () => {
    stopSpeaking();
    const combinedContent = articles
      .map((article) => article.content)
      .join(" ");
    speak(combinedContent, "all");
  };

  const chartData = {
    labels: categories,
    datasets: [
      {
        label: "新聞數量",
        data: fakeData,
        backgroundColor: [
          "rgba(75, 192, 192, 0.2)",
          "rgba(255, 99, 132, 0.2)",
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 206, 86, 0.2)",
          "rgba(153, 102, 255, 0.2)",
        ],
        borderColor: [
          "rgba(75, 192, 192, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(54, 162, 235, 1)",
          "rgba(255, 206, 86, 1)",
          "rgba(153, 102, 255, 1)",
        ],
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "新聞分類統計",
      },
    },
  };

  return (
    <div className="flex items-center justify-center bg-gradient-to-b from-gray-900 to-gray-800 text-white min-h-screen p-2">
      <div className="bg-gradient-to-b from-gray-900 to-gray-800 text-white min-h-screen p-5 animate-fade-in">
        <h1 className="text-4xl font-extrabold mb-6 text-center text-gradient ">
          每日新聞摘要
        </h1>

        <div className="flex justify-center space-x-4 mb-6">
          <button
            onClick={playing === null ? speakAll : stopSpeaking}
            className={`${
              playing === null
                ? "bg-blue-600 hover:bg-blue-700"
                : "bg-red-600 hover:bg-red-700"
            } text-white px-4 py-2 rounded flex items-center shadow-lg transition-transform transform hover:scale-110`}
          >
            {playing === null ? (
              <FaPlay className="mr-2" />
            ) : (
              <FaStop className="mr-2" />
            )}
            {playing === null ? "播放全部內容" : "停止播放"}
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {articles.map((article, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 0.5,
                delay: index * 0.2,
                ease: "easeOut",
              }}
              className="shadow-lg rounded-lg p-6 bg-gray-800 flex flex-col justify-between hover:shadow-2xl transition-all transform hover:scale-105 hover:bg-gray-700"
            >
              <h2 className="text-xl font-semibold mb-4 text-blue-400 flex items-center">
                <button
                  onClick={() => speak(article.content, index)}
                  className={`${
                    playing === index ? "animate-pulse" : ""
                  } text-white px-4 py-2 rounded hover:bg-green-600 shadow-md transition-all flex items-center`}
                >
                  {playing === index ? (
                    <FaVolumeUp className="mr-2" />
                  ) : (
                    <FaPlayCircle className="mr-2" />
                  )}
                </button>
                {article.title}
              </h2>
              <p className="text-gray-300 mb-4">{article.content}</p>
            </motion.div>
          ))}
        </div>
        <div className="p-4">
          <div className="text-center text-lg mb-4">
            共收集 <span className="font-bold text-blue-400">{totalNews}</span>{" "}
            篇新聞
          </div>
          <div className="mb-6">
            <Bar data={chartData} options={chartOptions} />
          </div>
        </div>
      </div>
    </div>
  );
}
