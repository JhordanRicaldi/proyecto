import React from 'react';

import ReactDOM from 'react-dom/client'
import './index.css';
import App from './App';

import { initializeApp } from "firebase/app";
import { firebaseConfig } from './firebase';

// Initialize Firebase
initializeApp(firebaseConfig);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)