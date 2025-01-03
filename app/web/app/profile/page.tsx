import React from "react";

type UserProfile = {
  name: string;
  email: string;
  bio: string;
};

const user: UserProfile = {
  name: "John Doe",
  email: "johndoe@example.com",
  bio: "A passionate developer who loves creating amazing web experiences.",
};

export default function Profile() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      <div className="max-w-md w-full p-6 bg-gray-800 rounded-lg shadow-lg">
        <div className="flex items-center space-x-4 mb-6">
          <div className="w-16 h-16 rounded-full overflow-hidden border-2 border-blue-500">
            <img
              src="/user.png"
              alt="User Avatar"
              className="w-full h-full object-cover"
            />
          </div>
          <div>
            <h2 className="text-2xl font-bold">{user.name}</h2>
            <p className="text-gray-400">{user.email}</p>
          </div>
        </div>
        <p className="text-gray-300 mb-4">{user.bio}</p>
        <hr className="border-gray-700 mb-4" />
        <div className="space-y-3">
          <a
            href="/settings"
            className="block bg-blue-600 hover:bg-blue-700 text-center py-2 rounded text-white font-bold transition"
          >
            Edit Profile
          </a>
          <a
            href="/logout"
            className="block bg-red-600 hover:bg-red-700 text-center py-2 rounded text-white font-bold transition"
          >
            Logout
          </a>
        </div>
      </div>
    </div>
  );
}
