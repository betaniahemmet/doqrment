import React, { useState, useEffect } from 'react';
import Button from './ui/button';
import PageWrapper from './ui/PageWrapper';


const TrackingLog = () => {
  const queryParams = new URLSearchParams(window.location.search);
  const trackingId = queryParams.get('tracking_id');
  const initials = queryParams.get('initials');
  const location = queryParams.get('location');

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
        setMinLabel(data.min_label || 'Not Anxious');
        setMaxLabel(data.max_label || 'Extremely Anxious');
        setAvailableActivities(data.activities.filter((a) => a && a.trim() !== ''));
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

  const handleSubmit = (e) => {
    e.preventDefault();
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
      .then((data) => console.log('✅ Server response:', data))
      .catch((err) => console.error('❌ Error submitting log:', err));
  };

  if (!trackingId || !initials || !location) {
    return (
       <PageWrapper>
          <h1 className="text-2xl font-bold text-red-600 mb-2">Invalid QR Link</h1>
          <p className="text-gray-700 text-sm">
            This link is missing tracking information. Please generate a new QR code.
          </p>
       </PageWrapper> 
    );
  }

  return (
    <PageWrapper>
      <form
        onSubmit={handleSubmit}
        className="relative z-10 w-full bg-white/90 p-6 rounded-lg shadow-md text-lg"
      >
        <h1 className="text-xl font-bold mb-4">{measurementType} Log</h1>
        <p className="text-lg text-gray-700 mb-6">
          Logging for <strong>{initials}</strong> at <strong>{location}</strong>
        </p>

        <div className="mb-6">
          <label htmlFor="slider" className="block text-lg text-gray-800 font-medium mb-2">
            {measurementType}: {value}
          </label>
          <input
            id="slider"
            type="range"
            min="1"
            max="10"
            value={value}
            onChange={handleValueChange}
            className="w-full h-4"
          />
          <div className="flex justify-between text-lg text-gray-600 mt-2">
            <span>{minLabel}</span>
            <span>{maxLabel}</span>
          </div>
        </div>

        {availableActivities.length > 0 && (
          <div className="mb-6">
            <label className="block text-lg text-gray-800 font-medium mb-2">Activities:</label>
            <div className="grid grid-cols-1 gap-y-3">
              {availableActivities.map((activity) => (
                <label key={activity} className="inline-flex items-center">
                  <input
                    type="checkbox"
                    checked={activities.includes(activity)}
                    onChange={() => toggleActivity(activity)}
                    className="mr-3 h-5 w-5"
                  />
                  <span className="text-lg">{activity}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        <div className="mt-6">
          <Button label="Log Entry" type="submit" />
        </div>
      </form>
    </PageWrapper>
  );
  };

export default TrackingLog;

