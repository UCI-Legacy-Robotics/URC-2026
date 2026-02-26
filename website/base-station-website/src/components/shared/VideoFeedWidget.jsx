'use client';

import { useState, useEffect, useRef } from 'react';

export default function VideoFeedWidget({ 
  feedName = "Camera Feed", 
  streamUrl = "", 
  type = "mjpeg", // 'mjpeg' or 'webrtc'
  fallbackText = "STANDBY"
}) {
  const [status, setStatus] = useState('connecting'); // 'connecting', 'live', 'error', 'offline'
  const videoRef = useRef(null);

  useEffect(() => {
    // If no URL is provided, keep it in standby/offline mode
    if (!streamUrl) {
      setStatus('offline');
      return;
    }

    if (type === 'mjpeg') {
      // MJPEG relies on the <img> tag loading the stream. 
      // We assume 'live' if the URL is present, but you can add an onError handler to the img tag.
      setStatus('live');
    }

    if (type === 'webrtc') {
      // Boilerplate for WebRTC connection
      setStatus('connecting');
      
      /* // Example WebRTC implementation:
        const peerConnection = new RTCPeerConnection(servers);
        
        // Listen for the stream
        peerConnection.ontrack = (event) => {
          if (videoRef.current) {
            videoRef.current.srcObject = event.streams[0];
            setStatus('live');
          }
        };

        // Handle connection drops
        peerConnection.oniceconnectionstatechange = () => {
          if (peerConnection.iceConnectionState === 'disconnected') {
            setStatus('error');
          }
        };
      */
    }

    // Cleanup function for when the component unmounts (though your single-page setup prevents this from happening often!)
    return () => {
      // e.g., peerConnection.close();
    };
  }, [streamUrl, type]);

  // Determine the status indicator color
  const getStatusColor = () => {
    switch(status) {
      case 'live': return '#4ade80'; // Green
      case 'connecting': return '#FFD200'; // Gold
      case 'error': return '#f87171'; // Red
      default: return '#555555'; // Gray
    }
  };

  return (
    <div style={{ 
      position: 'relative', 
      width: '100%', 
      height: '100%', 
      backgroundColor: '#0A0A0A', 
      borderRadius: '4px', 
      overflow: 'hidden', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center' 
    }}>
      
      {/* On-Screen Display (OSD) Overlay */}
      <div style={{ 
        position: 'absolute', 
        top: '10px', 
        left: '10px', 
        zIndex: 10, 
        backgroundColor: 'rgba(0,0,0,0.7)', 
        padding: '6px 12px', 
        borderRadius: '4px', 
        display: 'flex', 
        alignItems: 'center', 
        gap: '8px',
        border: '1px solid rgba(255,255,255,0.1)'
      }}>
        <div style={{ 
          width: '10px', 
          height: '10px', 
          borderRadius: '50%', 
          backgroundColor: getStatusColor(),
          boxShadow: status === 'live' ? `0 0 8px ${getStatusColor()}` : 'none'
        }}></div>
        <span style={{ color: '#fff', fontSize: '0.85rem', fontFamily: 'monospace', textTransform: 'uppercase', letterSpacing: '1px' }}>
          {feedName}
        </span>
      </div>

      {/* Media Elements */}
      {status === 'offline' || status === 'error' ? (
        <span style={{ color: '#555', fontFamily: 'monospace', letterSpacing: '2px' }}>
          [{status === 'error' ? 'CONNECTION LOST' : fallbackText}]
        </span>
      ) : type === 'mjpeg' ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img 
          src={streamUrl} 
          alt={feedName} 
          style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
          onError={() => setStatus('error')}
        />
      ) : (
        <video 
          ref={videoRef} 
          autoPlay 
          playsInline 
          muted 
          style={{ width: '100%', height: '100%', objectFit: 'cover' }} 
        />
      )}

    </div>
  );
}