import './src/index.css';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AdminPage from './AdminPage';
import TrackingLog from './TrackingLog';

const root = ReactDOM.createRoot(document.getElementById('app'));

root.render(
  <BrowserRouter>
    <Routes>
      <Route path="/admin" element={<AdminPage />} />
      <Route path="/log" element={<TrackingLog />} />
      <Route path="*" element={<div className="p-4 text-center text-red-500">404 - Not Found</div>} />
    </Routes>
  </BrowserRouter>
);