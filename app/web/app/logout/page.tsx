"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Logout() {
  const router = useRouter();
  // console.log(router);

  useEffect(() => {
    // 確保 router 是有效的
    if (!router) return; // 如果 router 為 null，則不執行後續代碼

    // 模擬登出處理
    setTimeout(() => {
      router.push("/login");
      // alert("You have been logged out.");
    }, 1000);
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-800 text-white">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-4">Logging Out...</h1>
        <p className="text-gray-400">Please wait while we log you out.</p>
      </div>
    </div>
  );
}
