"use client";
import { useState } from "react";

export default function NavbarWithState() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <nav className="bg-gray-900 p-4">
      <div className="flex justify-between items-center">
        <h1 className="text-white text-2xl">My App</h1>
        <button
          className="text-white"
          onClick={() => setIsMenuOpen((prev) => !prev)}
        >
          {isMenuOpen ? "Close Menu" : "Open Menu"}
        </button>
      </div>
      {isMenuOpen && (
        <div className="mt-4 bg-gray-800 p-4">
          <ul>
            <li className="text-white">Home</li>
            <li className="text-white">About</li>
            <li className="text-white">Contact</li>
          </ul>
        </div>
      )}
    </nav>
  );
}
