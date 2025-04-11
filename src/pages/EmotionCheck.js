import React, { useRef, useEffect, useState } from 'react';
import React, { useRef, useEffect, useState } from 'react';
import * as faceapi from 'face-api.js';

function EmotionCheck() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isRecording, setIsRecording] = useState(false);
  const [emotionStats, setEmotionStats] = useState({
    happy: 0,
    sad: 0,
    neutral: 0
  });

  useEffect(() => {
    loadModels();
  }, []);

  const loadModels = async () => {
    try {
      await Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
        faceapi.nets.faceExpressionNet.loadFromUri('/models')
      ]);
    } catch (error) {
      console.error('Error loading models:', error);
    }
  };

  const startVideo = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    } catch (error) {
      console.error('Error accessing webcam:', error);
    }
  };

  const startRecording = async () => {
    await startVideo();
    setIsRecording(true);
    startEmotionDetection();
  };

  const stopRecording = () => {
    setIsRecording(false);
    if (videoRef.current.srcObject) {
      videoRef.current.srcObject.getTracks().forEach(track => track.stop());
    }
  };

  const startEmotionDetection = async () => {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (video.readyState === 4) {
      const detections = await faceapi
        .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
        .withFaceExpressions();

      if (detections && detections.length > 0) {
        const expressions = detections[0].expressions;
        setEmotionStats(prev => ({
          happy: prev.happy + (expressions.happy > 0.5 ? 1 : 0),
          sad: prev.sad + (expressions.sad > 0.5 ? 1 : 0),
          neutral: prev.neutral + (expressions.neutral > 0.5 ? 1 : 0)
        }));
      }

      if (isRecording) {
        requestAnimationFrame(startEmotionDetection);
      }
    }
  };

  return (
    <div className="emotion-check">
      <h2>Emotion Check</h2>
      <div className="video-container">
        <video
          ref={videoRef}
          autoPlay
          muted
          style={{ width: '640px', height: '480px' }}
        />
        <canvas ref={canvasRef} style={{ position: 'absolute' }} />
      </div>
      <div className="controls">
        {!isRecording ? (
          <button onClick={startRecording}>Start Recording</button>
        ) : (
          <button onClick={stopRecording}>Stop Recording</button>
        )}
      </div>
      <div className="stats">
        <h3>Emotion Statistics:</h3>
        <p>Happy: {emotionStats.happy} frames</p>
        <p>Sad: {emotionStats.sad} frames</p>
        <p>Neutral: {emotionStats.neutral} frames</p>
      </div>
    </div>
  );
}

export default EmotionCheck;