"use client";
/* eslint-disable @next/next/no-img-element */
import React, { useState } from "react";
import { useRouter } from "next/navigation";

export default function Navbar() {
  const router = useRouter();
  const [isCardVisible, setIsCardVisible] = useState(false);

  const toggleCard = () => {
    setIsCardVisible(!isCardVisible);
  };

  return (
    <nav className="bg-gradient-to-r from-gray-800 to-gray-700 p-4 shadow-lg">
      <div className="container mx-auto flex items-center justify-between">
        {/* Logo Section */}
        <div className="flex items-center space-x-3">
          <img
            src="logo.png"
            alt="App Logo"
            className="w-10 h-10 object-contain"
          />
          <a href="/" className="text-2xl font-bold text-white">
            NewsSmart
          </a>
        </div>

        {/* User Section */}
        <div className="relative">
          <div
            className="flex items-center space-x-4 cursor-pointer"
            onClick={toggleCard}
          >
            <span className="text-white">Welcome, User!</span>
            <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-blue-400">
              <img
                src="user.png"
                alt="User"
                className="w-full h-full object-cover"
              />
            </div>
          </div>

          {/* User Info Card */}
          {isCardVisible && (
            <div className="absolute right-0 mt-2 w-64 bg-gray-800 text-white shadow-lg rounded-lg p-4 z-50">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 rounded-full overflow-hidden border-2 border-blue-400">
                  <img
                    src="user.png"
                    alt="User"
                    className="w-full h-full object-cover"
                  />
                </div>
                <div>
                  <h3 className="text-lg font-bold">John Doe</h3>
                  <p className="text-gray-400 text-sm">johndoe@example.com</p>
                </div>
              </div>
              <hr className="my-3 border-gray-700" />
              <ul className="space-y-2">
                <li>
                  <a
                    href="/profile"
                    className="block text-gray-300 hover:text-white transition"
                  >
                    View Profile
                  </a>
                </li>
                <li>
                  <a
                    href="/settings"
                    className="block text-gray-300 hover:text-white transition"
                  >
                    Account Settings
                  </a>
                </li>
                <li>
                  <button
                    onClick={() => router.push("/logout")}
                    className="block text-gray-300 hover:text-white transition w-full text-left"
                  >
                    Logout
                  </button>
                </li>
              </ul>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
