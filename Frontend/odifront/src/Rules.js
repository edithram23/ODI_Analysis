import './Analysis.css';
import React, { useEffect, useState, useRef } from 'react';
import Modal from 'react-modal';
import Output from './Output';
const URL = process.env.REACT_APP_URL;

// Modal styling
const customStyles = {
    content: {
        top: '50%',
        left: '50%',
        right: 'auto',
        bottom: 'auto',
        marginRight: '-50%',
        transform: 'translate(-50%, -50%)',
        textAlign: 'center',
        backgroundColor: '#202222',
        color: '#FFFFFF',
        borderRadius: '10px',
        padding: '20px',
        border: 'none',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
    },
    overlay: {
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
    },
};

async function Submit(user_text, set_text, setLoading, set_vis) {
    if (user_text.trim() !== '') {
        setLoading(true);
        const body = { input: user_text };

        try {
            const response = await fetch(`${URL}/api/rule`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });

            const data = await response.json();
            if (Array.isArray(data.Output)) {
                const arr = data.Output.map((val, index) => <li key={index}>{val}</li>);
                set_text(arr);
            } else {
                throw new Error('Invalid Output format');
            }
        } catch (error) {
            console.error('Error fetching rule:', error);
            set_text(<li>Error fetching data</li>);
        }
        setLoading(false);
    } else {
        set_text('Retry!');
    }
}

async function SubmitAudio(audioBlob, set_text, audioRef, setLoading, set_vis) {
    const formData = new FormData();
    formData.append('audio', audioBlob, 'recording.wav');
    setLoading(true);

    try {
        const response = await fetch(`${URL}/api/ruleaudio`, {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        const arr = data.Output.map((val, index) => <li key={index}>{val}</li>);
        set_text(arr);

        // set_text(arr);
        console.log(arr);

        if (data.audio) {
            const audioBlob = base64ToBlob(data.audio, 'audio/wav');
            const audioUrl = window.URL.createObjectURL(audioBlob); // Use window.URL
            audioRef.current.src = audioUrl;
            await audioRef.current.play(); // Play the audio
        }
    } catch (error) {
        console.error('Error processing audio:', error);
    }

    setLoading(false);
}

function base64ToBlob(base64, contentType) {
    const byteCharacters = atob(base64);
    const byteNumbers = Array.from(byteCharacters, (char) => char.charCodeAt(0));
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: contentType });
}

function Rules() {
    const [text, set_text] = useState('');
    const [answer, setAnswer] = useState('');
    const [loading, setLoading] = useState(false);
    const [vis, set_vis] = useState(true);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const mediaRecorderRef = useRef(null);
    const audioChunks = useRef([]);
    const audioRef = useRef(new Audio());

    const handleSubmit = (e) => {
        e.preventDefault();
        Submit(text, setAnswer, setLoading, set_vis);
        set_vis(false);
    };

    const openModal = () => setIsModalOpen(true);
    const closeModal = () => setIsModalOpen(false);

    const handleStartRecording = () => {    setLoading(true);
        set_vis(false);

        navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
            mediaRecorderRef.current = new MediaRecorder(stream);
            audioChunks.current = [];

            mediaRecorderRef.current.ondataavailable = (event) => {
                audioChunks.current.push(event.data);
            };

            mediaRecorderRef.current.onstop = () => {
                const audioBlob = new Blob(audioChunks.current, { type: 'audio/wav' });
                SubmitAudio(audioBlob, setAnswer, audioRef, setLoading, set_vis);
                closeModal();
            };

            mediaRecorderRef.current.start();
            setTimeout(() => handleStopRecording(), 30000);
        });
    };

    const handleStopRecording = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
            mediaRecorderRef.current.stop();
        }
        setLoading(false);

        // mediaRecorderRef.current.stop();

    };

    return (
        <div className="Container">
            <div className="InnerContainer">
                <h1>AUDIO Q&A</h1>
            </div>
            <div className="search-container">
                <form className="forms" onSubmit={handleSubmit}>
                    <input
                        type="text"
                        placeholder="Search..."
                        className="search"
                        value={text}
                        onChange={(e) => set_text(e.target.value)}
                    />
                    <button type="submit" className="submit-button">
                            <i className="fa fa-search"></i>
                        </button>
                        
                        
                </form>
                <button type="button" onClick={openModal} className="voice-button">
                            <i className="fa fa-microphone"></i>
                        </button>
                
            </div>
            <Modal
                isOpen={isModalOpen}
                onRequestClose={closeModal}
                style={customStyles}
                contentLabel="Voice Recorder"
            >
                <h2>Voice Recorder</h2>
                <button onClick={handleStartRecording} className="modal-button">
                    Start Recording
                </button>
                <button onClick={handleStopRecording} className="modal-button">
                    Stop Recording
                </button>
                <button onClick={closeModal} className="modal-button">
                    Close
                </button>
                {loading ? (
                    <div>Recording ON...</div>
                ) : (
                    <>
                        
                    </>
                )}
            </Modal>
            <div className="InnerContainer">
                {loading ? (
                    <div>Loading...</div>
                ) : (
                    <>
                        <Output answer={answer} vis={vis} compare={false} />
                    </>
                )}
            </div>
        </div>
    );
}

export default Rules;
