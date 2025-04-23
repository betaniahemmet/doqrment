import React, { useState, useEffect } from 'react';
import Button from './ui/button';
import PageWrapperMobile from './ui/PageWrapperMobile';


const TrackingLog = () => {
  const queryParams = new URLSearchParams(window.location.search);
  const trackingId = queryParams.get('tracking_id');
  const initials = queryParams.get('initials');
  const location = queryParams.get('location');
  const [lastSubmitted, setLastSubmitted] = useState(null);


  const [focus, setFocus] = useState('Mood');
  const [trackingMode, setTrackingMode] = useState("scale");
  const [minLabel, setMinLabel] = useState('Not Anxious');
  const [maxLabel, setMaxLabel] = useState('Extremely Anxious');
  const [value, setValue] = useState(5);
  const [activities, setActivities] = useState([]);
  const [availableActivities, setAvailableActivities] = useState([]);

  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');


  useEffect(() => {
    fetch(`/get-admin-settings?tracking_id=${trackingId}`)
      .then((res) => res.json())
      .then((data) => {
        setFocus(data.focus);
        setMinLabel(data.min_label || 'Not Anxious');
        setMaxLabel(data.max_label || 'Extremely Anxious');
        setAvailableActivities(data.activities.filter((a) => a && a.trim() !== ''));
        setTrackingMode(data.tracking_mode || "scale");
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
    setSuccessMessage('');
    setErrorMessage('');

    // Check if last submission was less than 60 seconds ago
    if (lastSubmitted && Date.now() - lastSubmitted < 60000) {
      setErrorMessage('Vänta minst en minut mellan loggningar.');
      return;
    }

    const logData = {
      tracking_id: trackingId,
      initials,
      location,
      focus: focus,
      activities,
      timestamp: new Date().toISOString(),
    };

    if (trackingMode === "scale") {
      logData.value = value;
    } else {
      logData.value = 1; // log event occurrence as +1
    }

    fetch('/log', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(logData),
    })
      .then((res) => {
      if (!res.ok) throw new Error('Servern returnerar ett fel');
      return res.json();
    })
      .then(() => {
      setSuccessMessage('Loggningen sparades.');
      setLastSubmitted(Date.now());
    })
    .catch(() => {
      setErrorMessage('Kunde inte kontakta servern');
    }); 
  };

  if (!trackingId || !initials || !location) {
    return (
       <PageWrapperMobile>
          <h1 className="text-2xl font-bold text-red-600 mb-2">Invalid QR Link</h1>
          <p className="text-gray-700 text-sm">
            This link is missing tracking information. Please generate a new QR code.
          </p>
       </PageWrapperMobile> 
    );
  }

  return (
    <PageWrapperMobile>
      <form
        onSubmit={handleSubmit}
        className="relative z-10 w-full bg-white/90 p-6 rounded-lg shadow-md text-lg"
      >
        <h1 className="text-xl font-bold mb-4">{focus}-Mätning</h1>
        <p className="text-lg text-gray-700 mb-6">
          För <strong>{initials}</strong> at <strong>{location}</strong>
        </p>

        {trackingMode === 'scale' && (
          <div className="mb-6">
            <label htmlFor="slider" className="block text-lg text-gray-800 font-medium mb-2">
              {focus}: {value}
            </label>
            <input
              id="slider"
              type="range"
              min="1"
              max="10"
              value={value}
              onChange={handleValueChange}
              className="w-full h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer focus:outline-none accent-blue-600"
            />
            <div className="flex justify-between text-lg text-gray-600 mt-2">
              <span>{minLabel}</span>
              <span>{maxLabel}</span>
            </div>
          </div>
        )}


        {availableActivities.length > 0 && (
          <div className="mb-6">
            <label className="block text-lg text-gray-800 font-medium mb-2">Aktivitet för tillfället:</label>
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
          {successMessage && <p className="mt-4 text-green-600">{successMessage}</p>}
          {errorMessage && <p className="mt-4 text-red-600">{errorMessage}</p>}

          <Button label="Spara" type="submit" />
        </div>
      </form>
    </PageWrapperMobile>
  );
  };

export default TrackingLog;

