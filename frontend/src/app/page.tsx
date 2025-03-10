"use client";
import { useState, useEffect } from "react";
import axios from "axios";
import Image from "next/image";

export default function Home() {
  const [answers, setAnswers] = useState<Record<string, number>>({});
  const [question, setQuestion] = useState<string>("Is it an animal?");
  const [result, setResult] = useState<string>("");
  const [confidence, setConfidence] = useState<number>(0);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [feedback, setFeedback] = useState<string>("");
  const [userEntity, setUserEntity] = useState<string>("");
  const [gameCount, setGameCount] = useState<number>(0);
  const [showIntro, setShowIntro] = useState<boolean>(true);
  const [debugInfo, setDebugInfo] = useState<any>(null);

  const handleAnswer = async (answer: boolean) => {
    setIsLoading(true);
    const newAnswers = { ...answers, [question]: answer ? 1 : 0 };
    setAnswers(newAnswers);

    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", { answers: newAnswers });
      
      if (response.data.prediction) {
        setResult(response.data.prediction);
        setConfidence(response.data.confidence || 0);
      } else if (response.data.next_question) {
        setQuestion(response.data.next_question);
      } else {
        setResult("I don't know what you're thinking of!");
        setConfidence(0);
      }
    } catch (error) {
      console.error("Error making prediction:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedback = async (isCorrect: boolean) => {
    if (isCorrect) {
      setFeedback("Great! I guessed correctly.");
      await axios.post("http://127.0.0.1:8000/feedback", {
        entity: result,
        correct: true,
        answers
      });
    } else {
      setFeedback("I was wrong. What were you thinking of?");
    }
  };

  const submitEntity = async () => {
    if (userEntity.trim()) {
      await axios.post("http://127.0.0.1:8000/feedback", {
        entity: userEntity,
        correct: true,
        answers
      });
      setFeedback(`Thanks! I'll remember that ${userEntity} has these attributes.`);
      setUserEntity("");
    }
  };

  const resetGame = () => {
    setAnswers({});
    setQuestion("Is it an animal?");
    setResult("");
    setConfidence(0);
    setFeedback("");
    setUserEntity("");
    setGameCount(prev => prev + 1);
  };

  const startGame = () => {
    setShowIntro(false);
  };

  const toggleDebug = async () => {
    if (debugInfo) {
      setDebugInfo(null);
    } else {
      try {
        const response = await axios.get("http://127.0.0.1:8000/debug");
        setDebugInfo(response.data);
      } catch (error) {
        console.error("Error fetching debug info:", error);
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800 text-white">
      {showIntro ? (
        <div className="w-full max-w-2xl p-8 bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl text-center border border-white/20 animate-fade-in">
          <h1 className="text-5xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-pink-500 to-indigo-500">
            Akinator AI
          </h1>
          <p className="text-xl mb-8 text-white/80">
            Think of something, and I'll try to guess it through a series of questions.
            The more you play, the smarter I become!
          </p>
          <div className="mb-10 relative h-64 w-64 mx-auto">
            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 animate-pulse"></div>
            <div className="absolute inset-2 rounded-full bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-800"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-6xl">🧠</span>
            </div>
          </div>
          <button
            onClick={startGame}
            className="px-8 py-4 bg-gradient-to-r from-pink-500 to-indigo-600 rounded-full text-xl font-bold shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
          >
            Start Guessing
          </button>
        </div>
      ) : (
        <div className="w-full max-w-2xl p-8 bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl border border-white/20 animate-fade-in">
          <h1 className="text-4xl font-bold text-center mb-6 bg-clip-text text-transparent bg-gradient-to-r from-pink-500 to-indigo-500">
            Akinator AI
          </h1>
          
          {isLoading ? (
            <div className="flex flex-col items-center justify-center my-12">
              <div className="w-20 h-20 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mb-4"></div>
              <p className="text-xl text-white/70">Thinking...</p>
            </div>
          ) : !result ? (
            <div className="space-y-8">
              <div className="p-6 bg-white/5 rounded-xl border border-white/10">
                <p className="text-2xl text-center font-medium">{question}</p>
              </div>
              
              <div className="flex justify-center gap-6">
                <button 
                  className="flex-1 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-6 py-4 rounded-xl text-xl font-medium shadow-lg transform hover:scale-105 transition-all duration-200"
                  onClick={() => handleAnswer(true)}
                >
                  Yes
                </button>
                <button 
                  className="flex-1 bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 text-white px-6 py-4 rounded-xl text-xl font-medium shadow-lg transform hover:scale-105 transition-all duration-200"
                  onClick={() => handleAnswer(false)}
                >
                  No
                </button>
              </div>
              
              <div className="text-center text-white/60 text-sm">
                Question {Object.keys(answers).length + 1}
              </div>
            </div>
          ) : (
            <div className="text-center space-y-8">
              <div className="relative">
                <div className="absolute -inset-1 bg-gradient-to-r from-pink-500 to-indigo-500 rounded-2xl blur opacity-75"></div>
                <div className="relative p-6 bg-black/40 rounded-xl">
                  <h2 className="text-2xl font-medium mb-2">I think it's a...</h2>
                  <p className="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-indigo-400 mb-2">
                    {result}
                  </p>
                  <div className="w-full bg-white/10 rounded-full h-4 mb-2">
                    <div 
                      className="bg-gradient-to-r from-pink-500 to-indigo-500 h-4 rounded-full transition-all duration-1000 ease-out"
                      style={{ width: `${Math.round(confidence * 100)}%` }}
                    ></div>
                  </div>
                  <p className="text-white/70">Confidence: {Math.round(confidence * 100)}%</p>
                </div>
              </div>
              
              {!feedback ? (
                <div className="flex justify-center gap-4">
                  <button 
                    className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-6 py-3 rounded-xl font-medium shadow-lg transform hover:scale-105 transition-all duration-200"
                    onClick={() => handleFeedback(true)}
                  >
                    Correct!
                  </button>
                  <button 
                    className="bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700 text-white px-6 py-3 rounded-xl font-medium shadow-lg transform hover:scale-105 transition-all duration-200"
                    onClick={() => handleFeedback(false)}
                  >
                    Wrong
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  <p className="text-xl">{feedback}</p>
                  {feedback.includes("wrong") && (
                    <div className="flex gap-2">
                      <input
                        type="text"
                        value={userEntity}
                        onChange={(e) => setUserEntity(e.target.value)}
                        placeholder="What were you thinking of?"
                        className="flex-1 px-4 py-3 bg-white/10 border border-white/20 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                      <button
                        onClick={submitEntity}
                        className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white px-4 py-3 rounded-xl font-medium shadow-lg"
                      >
                        Submit
                      </button>
                    </div>
                  )}
                </div>
              )}
              
              <button
                onClick={resetGame}
                className="mt-6 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-medium shadow-lg transform hover:scale-105 transition-all duration-200"
              >
                Play Again
              </button>
            </div>
          )}
          
          <div className="mt-8 pt-6 border-t border-white/10 text-center text-white/40 text-sm">
            Games played: {gameCount}
          </div>
        </div>
      )}
      {debugInfo && (
        <div className="mt-8 p-4 bg-black/30 rounded-lg text-xs font-mono overflow-auto max-h-60">
          <div className="flex justify-between mb-2">
            <h3 className="font-bold">Debug Info</h3>
            <button onClick={toggleDebug} className="text-white/60 hover:text-white">Close</button>
          </div>
          <pre>{JSON.stringify(debugInfo, null, 2)}</pre>
        </div>
      )}
      <div className="absolute bottom-4 left-4">
        <button 
          onClick={toggleDebug}
          className="text-white/40 hover:text-white/70 text-xs px-2 py-1 bg-white/10 rounded"
        >
          Debug
        </button>
      </div>
    </div>
  );
}