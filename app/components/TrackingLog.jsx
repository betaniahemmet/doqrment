import React, { useState, useEffect } from 'react';
import Button from './ui/button';

const TrackingLog = () => {
  const queryParams = new URLSearchParams(window.location.search);
  const trackingId = queryParams.get("tracking_id");
  const initials = queryParams.get("initials");
  const location = queryParams.get("location");

  const [measurementType, setMeasurementType] = useState('Mood');
  const [minLabel, setMinLabel] = useState('Not Anxious');
  const [maxLabel, setMaxLabel] = useState('Extremely Anxious');
  const [value, setValue] = useState(5);
  const [activities, setActivities] = useState([]);
  const [availableActivities, setAvailableActivities] = useState([]);

  useEffect(() => {
    fetch(`/get-admin-settings?tracking_id=${trackingId}`)
      .then((res) => res.json())
      .then((data) => {
        setMeasurementType(data.measurement);
        setMinLabel(data.min_label ?? 'Not Anxious');
        setMaxLabel(data.max_label ?? 'Extremely Anxious');
        setAvailableActivities(data.activities || []);
      })
      .catch((err) => console.error('Error loading admin settings:', err));
  }, [trackingId]);

  const handleValueChange = (e) => {
    setValue(parseInt(e.target.value, 10));
  };

  const toggleActivity = (activity) => {
    setActivities((prev) =>
      prev.includes(activity)
        ? prev.filter((a) => a !== activity)
        : [...prev, activity]
    );
  };

  const handleSubmit = () => {
    const logData = {
      tracking_id: trackingId,
      initials,
      location,
      measurement_type: measurementType,
      value,
      activities,
      timestamp: new Date().toISOString(),
    };

    fetch('/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(logData),
    })
      .then((res) => res.json())
      .then((data) => console.log('Server response:', data))
      .catch((err) => console.error('Error submitting log:', err));
  };

  if (!trackingId || !initials || !location) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
        <div className="max-w-md bg-white p-6 rounded shadow text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-2">Invalid QR Link</h1>
          <p className="text-gray-700 text-sm">
            This link is missing tracking information. Please generate a new QR code.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
      <div className="max-w-xl w-full bg-white p-6 rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-2">{measurementType} Log</h1>
        <p className="text-sm text-gray-600 mb-4">
          Logging for <strong>{initials}</strong> at <strong>{location}</strong>
        </p>

        <div className="mb-6">
          <label htmlFor="slider" className="block text-gray-700 font-medium mb-1">
            {measurementType}: {value}
          </label>
          <input
            id="slider"
            type="range"
            min="1"
            max="10"
            value={value}
            onChange={handleValueChange}
            className="w-full"
          />
          <div className="flex justify-between text-sm text-gray-600 mt-1">
            <span>{minLabel}</span>
            <span>{maxLabel}</span>
          </div>
        </div>

        <div className="mb-6">
          <label className="block text-gray-700 font-medium mb-2">Activities:</label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {availableActivities.map((activity) => (
              <label key={activity} className="inline-flex items-center">
                <input
                  type="checkbox"
                  checked={activities.includes(activity)}
                  onChange={() => toggleActivity(activity)}
                  className="mr-2"
                />
                {activity}
              </label>
            ))}
          </div>
        </div>

        <Button label="Log Entry" onClick={handleSubmit} />
      </div>
    </div>
  );
};

export default TrackingLog;

