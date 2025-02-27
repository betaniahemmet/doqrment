import React, { useState } from 'react';
import Button from './ui/button'; // Importing the reusable Button component

const MoodActivityLog = () => {
    // State to store the mood and selected activities
    const [mood, setMood] = useState(50); // Default mood value is 50 (middle of the range)
    const [activities, setActivities] = useState([]);

    // List of available activities (these can be customized)
    const availableActivities = [
        'Reading',
        'Listening to Music',
        'Physical Exercise',
        'Social Interaction',
        'Relaxing'
    ];

    // Handle mood slider change
    const handleMoodChange = (e) => {
        setMood(e.target.value);
    };

    // Handle activity checkbox changes
    const handleActivityChange = (activity) => {
        if (activities.includes(activity)) {
            setActivities(activities.filter((a) => a !== activity));
        } else {
            setActivities([...activities, activity]);
        }
    };

    // Handle form submission
    const handleSubmit = () => {
        const logData = {
            mood: parseInt(mood, 10),
            activities,
            timestamp: new Date().toISOString()
        };
        
        console.log('Log submitted:', logData);

        fetch('/log', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(logData)
        })
        .then(response => response.json())
        .then(data => console.log('Server response:', data))
        .catch(error => console.error('Error:', error));
    };

    return (
        <div className="p-4 max-w-md mx-auto bg-white shadow-lg rounded-lg">
            <h1 className="text-2xl mb-4 font-bold">Mood & Activity Logging</h1>
            
            <div className="mb-4">
                <label htmlFor="mood-slider" className="block mb-2">
                    Mood: {mood}
                </label>
                <input
                    id="mood-slider"
                    type="range"
                    min="0"
                    max="100"
                    value={mood}
                    onChange={handleMoodChange}
                    className="w-full"
                />
                <div className="flex justify-between text-sm text-gray-600">
                    <span>Very Calm</span>
                    <span>Violent</span>
                </div>
            </div>

            <div className="mb-4">
                <label className="block mb-2 text-gray-600">Activities:</label>
                {availableActivities.map((activity) => (
                    <div key={activity} className="flex items-center mb-1">
                        <input
                            type="checkbox"
                            id={activity}
                            checked={activities.includes(activity)}
                            onChange={() => handleActivityChange(activity)}
                            className="mr-2"
                        />
                        <label htmlFor={activity}>{activity}</label>
                    </div>
                ))}
            </div>

            <Button label="Log Mood & Activities" onClick={handleSubmit} />
        </div>


    );
};

export default MoodActivityLog;

