import React, { useState } from 'react';
import Button from './ui/button';
import PageWrapper from './ui/PageWrapper';


const AdminPage = () => {
  const [formData, setFormData] = useState({
    measurement_type: 'Mood',
    min_label: '',
    max_label: '',
    activities: ['', '', '', '', '', ''],
    initials: '',
    location: 'Verkstan',
    duration: 'week',
    admin_email: '',
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleActivityChange = (index, value) => {
    const updated = [...formData.activities];
    updated[index] = value;
    setFormData((prev) => ({ ...prev, activities: updated }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("✅ Form submit triggered");
    const form = new FormData();
    Object.entries(formData).forEach(([key, val]) => {
      if (key === 'activities') {
        formData.activities.forEach((act, i) => {
          form.append(`activity_${i + 1}`, act);
        });
      } else {
        form.append(key, val);
      }
    });

    // 👉 This is just for debugging
    for (let pair of form.entries()) {
      console.log(`${pair[0]}: ${pair[1]}`);
    }

    // ✅ Only send the request once
    const res = await fetch('/admin', {
      method: 'POST',
      body: form,
    });


    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${formData.initials}_${formData.location}_QR.pdf`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  };

  return (
    <PageWrapper>
      <form onSubmit={handleSubmit} className="bg-white/90 w-full max-w-2xl mx-auto bg-white shadow-md rounded-lg p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Create Tracking QR</h1>


        <div className="mb-4">
          <label className="block font-medium mb-1">Measurement:</label>
          <input
            type="text"
            name="measurement_type"
            value={formData.measurement_type}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
          />
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block font-medium mb-1">Min Label:</label>
            <input
              type="text"
              name="min_label"
              value={formData.min_label}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            />
          </div>
          <div>
            <label className="block font-medium mb-1">Max Label:</label>
            <input
              type="text"
              name="max_label"
              value={formData.max_label}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            />
          </div>
        </div>

        <div className="mb-4">
          <label className="block font-medium mb-1">Activities (up to 6):</label>
          <div className="grid grid-cols-2 gap-2">
            {formData.activities.map((act, i) => (
              <input
                key={i}
                type="text"
                value={act}
                onChange={(e) => handleActivityChange(i, e.target.value)}
                className="border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
              />
            ))}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block font-medium mb-1">Initials:</label>
            <input
              type="text"
              name="initials"
              maxLength={2}
              value={formData.initials}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            />
          </div>

          <div>
            <label className="block font-medium mb-1">Location:</label>
            <select
              name="location"
              value={formData.location}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            >
              <option value="Verkstan">Verkstan</option>
              <option value="Kusten">Kusten</option>
              <option value="Konferensen">Konferensen</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block font-medium mb-1">Duration:</label>
            <select
              name="duration"
              value={formData.duration}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            >
              <option value="week">Week</option>
              <option value="month">Month</option>
            </select>
          </div>

          <div>
            <label className="block font-medium mb-1">Email:</label>
            <input
              type="admin_email"
              name="admin_email"
              value={formData.email}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            />
          </div>
        </div>

        <Button label="Generate QR Code" type="submit" />
      </form>
    </PageWrapper>
  );
};

export default AdminPage;
