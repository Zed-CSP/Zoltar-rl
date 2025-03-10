"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import Link from "next/link";

export default function AdminPage() {
  const [questions, setQuestions] = useState<string[]>([]);
  const [newQuestion, setNewQuestion] = useState("");
  const [entities, setEntities] = useState<Record<string, Record<string, number>>>({});
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:8000/admin/data");
      setQuestions(response.data.questions);
      setEntities(response.data.entities);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddQuestion = async () => {
    if (!newQuestion.trim()) return;
    
    try {
      await axios.post("http://127.0.0.1:8000/add-question", null, {
        params: { question: newQuestion }
      });
      setMessage(`Question "${newQuestion}" added successfully!`);
      setNewQuestion("");
      fetchData();
      
      // Clear message after 3 seconds
      setTimeout(() => setMessage(""), 3000);
    } catch (error) {
      console.error("Error adding question:", error);
      setMessage("Error adding question. Please try again.");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 text-white p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-pink-500 to-indigo-500">
            Akinator Admin
          </h1>
          <Link 
            href="/"
            className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition-colors"
          >
            Back to Game
          </Link>
        </div>

        {message && (
          <div className="mb-6 p-4 bg-green-500/20 border border-green-500/30 rounded-lg">
            {message}
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <h2 className="text-2xl font-semibold mb-4">Add New Question</h2>
            <div className="flex gap-2 mb-6">
              <input
                type="text"
                value={newQuestion}
                onChange={(e) => setNewQuestion(e.target.value)}
                placeholder="Enter a yes/no question..."
                className="flex-1 px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <button
                onClick={handleAddQuestion}
                className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white px-4 py-3 rounded-xl font-medium shadow-lg"
              >
                Add
              </button>
            </div>
            <div className="text-white/70 text-sm">
              <p>Tips for good questions:</p>
              <ul className="list-disc pl-5 mt-2 space-y-1">
                <li>Make sure it can be answered with yes/no</li>
                <li>Be specific and clear</li>
                <li>Avoid subjective questions</li>
                <li>Consider questions that divide entities well</li>
              </ul>
            </div>
          </div>

          <div className="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
            <h2 className="text-2xl font-semibold mb-4">Current Questions</h2>
            {loading ? (
              <div className="flex justify-center py-8">
                <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
              </div>
            ) : (
              <div className="max-h-96 overflow-y-auto pr-2 custom-scrollbar">
                <ul className="space-y-2">
                  {questions.map((q, index) => (
                    <li key={index} className="p-3 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                      {q}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        <div className="mt-8 bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
          <h2 className="text-2xl font-semibold mb-4">Known Entities</h2>
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="w-10 h-10 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {Object.keys(entities).map((entity) => (
                <div key={entity} className="p-4 bg-white/5 rounded-lg hover:bg-white/10 transition-colors">
                  <h3 className="font-medium text-lg mb-2">{entity}</h3>
                  <div className="text-sm text-white/70">
                    {Object.keys(entities[entity]).length} attributes
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="absolute bottom-4 right-4">
          <Link 
            href="/admin"
            className="text-white/40 hover:text-white/70 text-sm underline transition-colors"
          >
            Admin
          </Link>
        </div>
      </div>
    </div>
  );
}