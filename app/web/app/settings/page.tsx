"use client";
import React, { useState } from "react";
import { useRouter } from "next/navigation";

type UserProfile = {
  name: string;
  email: string;
  bio: string;
};

const SettingsPage = () => {
  const [user, setUser] = useState<UserProfile>({
    name: "John Doe",
    email: "johndoe@example.com",
    bio: "A passionate developer who loves creating amazing web experiences.",
  });

  const [editedUser, setEditedUser] = useState<UserProfile>(user);
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setEditedUser((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSave = () => {
    setUser(editedUser);
    // You can also handle saving the user data to a server here
    router.push("/profile"); // Redirect to profile page
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-gray-900 to-gray-800 text-white">
      <div className="max-w-md w-full p-6 bg-gray-800 rounded-lg shadow-lg">
        <h2 className="text-3xl font-bold mb-6">Edit Profile</h2>
        <div className="space-y-4">
          <div>
            <label htmlFor="name" className="block text-gray-300">
              Name
            </label>
            <input
              type="text"
              name="name"
              id="name"
              value={editedUser.name}
              onChange={handleChange}
              className="w-full p-2 bg-gray-700 rounded text-white"
            />
          </div>
          <div>
            <label htmlFor="email" className="block text-gray-300">
              Email
            </label>
            <input
              type="email"
              name="email"
              id="email"
              value={editedUser.email}
              onChange={handleChange}
              className="w-full p-2 bg-gray-700 rounded text-white"
            />
          </div>
          <div>
            <label htmlFor="bio" className="block text-gray-300">
              Bio
            </label>
            <textarea
              name="bio"
              id="bio"
              value={editedUser.bio}
              onChange={handleChange}
              className="w-full p-2 bg-gray-700 rounded text-white"
              rows={4}
            />
          </div>
        </div>
        <div>
          <div className="space-y-3 mt-6 flex justify-center">
            <button
              onClick={handleSave}
              className="w-full bg-blue-600 hover:bg-blue-700 text-center py-2 rounded text-white font-bold transition shadow-lg hover:shadow-xl mx-2"
            >
              Save Changes
            </button>
            <button
              onClick={() => router.push("/profile")}
              className="w-full bg-gray-600 hover:bg-gray-700 text-center py-2 rounded text-white font-bold transition shadow-lg hover:shadow-xl mx-2"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
