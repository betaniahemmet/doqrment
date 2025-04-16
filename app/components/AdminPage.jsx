import React, { useState } from 'react';
import Button from './ui/button';
import PageWrapperDesktop from './ui/PageWrapperDesktop'; //Because intended for desktop


const AdminPage = () => {
  
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [formData, setFormData] = useState({
    measurement_type: '',
    min_label: '',
    max_label: '',
    activities: ['', '', '', '', '', ''],
    initials: '',
    location: '',
    duration: '',
    admin_email: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    // Auto-uppercase initials
    if (name === 'initials') {
      setFormData((prev) => ({
        ...prev,
        initials: value.toUpperCase(),
      }));
      return;
    }

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleActivityChange = (index, value) => {
    const updated = [...formData.activities];
    updated[index] = value;
    setFormData((prev) => ({ ...prev, activities: updated }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccessMessage('');
    setErrorMessage('');

    // Required field validation
    if (!formData.measurement_type.trim()) {
      setErrorMessage("Fältet 'Vad mäts' måste fyllas i.");
      return;
    }

    if (!formData.min_label.trim() || !formData.max_label.trim()) {
      setErrorMessage("Min och max etikett måste fyllas i.");
      return;
    }

    if (!formData.initials.trim()) {
      setErrorMessage("Initialer måste anges.");
      return;
    }

    if (!formData.location) {
      setErrorMessage("Du måste välja en verksamhet.");
      return;
    }

    if (!formData.duration) {
      setErrorMessage("Du måste välja en tidsperiod.");
      return;
    }

    if (!formData.admin_email.trim()) {
      setErrorMessage("En e-postadress måste anges.");
      return;
    }

    const normalizedEmail = formData.admin_email.toLowerCase();
    if (!normalizedEmail.endsWith("@betaniahemmet.se")) {
      setErrorMessage("E-postadressen måste sluta med @betaniahemmet.se.");
      return;
    }
    setFormData((prev) => ({
      ...prev,
      admin_email: normalizedEmail,
    }));

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

    for (let pair of form.entries()) {
      console.log(`${pair[0]}: ${pair[1]}`);
    }

    try {
      const res = await fetch('/admin', {
        method: 'POST',
        body: form,
      });
    
    if (!res.ok) {
      const errorText = await res.text();
      if (errorText.includes("finns redan")) {
        setErrorMessage("En kartläggning för dessa initialer och platsen finns redan.");
      } else {
        setErrorMessage("Serverfel – kunde inte skapa QR-kod.");
      }
      return;
    }


      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${formData.initials}_${formData.location}_QR.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();

      setSuccessMessage('QR-koden har skapats och laddats ner.');
      setFormData({
      measurement_type: '',
      min_label: '',
      max_label: '',
      activities: ['', '', '', '', '', ''],
      initials: '',
      location: '',
      duration: '',
      admin_email: '',
      });
    } catch (error) {
      console.error('❌ Error:', error);
      setErrorMessage('Något gick fel. Kontrollera fälten och försök igen.');
    }
  };


  return (
    <PageWrapperDesktop>
      <form onSubmit={handleSubmit} className="bg-white/90 w-full max-w-5xl mx-auto shadow-md rounded-lg p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">Skapa QR för kartläggning</h1>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block font-medium mb-1">Vad ska mätas?:</label>
            <input
              type="text"
              name="measurement_type"
              value={formData.measurement_type}
              onChange={handleChange}
              placeholder="Ex: Trötthet"
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            />
          </div>
          <div>
            <label className="block font-medium mb-1">Initialer:</label>
            <input
              type="text"
              name="initials"
              maxLength={2}
              value={formData.initials}
              onChange={handleChange}
              placeholder="Ex: AB"
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            />
          </div>
        </div>

        {/* Min/Max Labels */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block font-medium mb-1">Minsta-Läge:</label>
            <input
              type="text"
              name="min_label"
              value={formData.min_label}
              onChange={handleChange}
              placeholder="Ex: Trött"
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            />
          </div>
          <div>
            <label className="block font-medium mb-1">Mesta-Läge:</label>
            <input
              type="text"
              name="max_label"
              value={formData.max_label}
              onChange={handleChange}
              placeholder="Ex: Pigg"
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            />
          </div>
        </div>

        {/* Activities */}
        <div>
          <label className="block font-medium mb-1">Aktiviteter (Max 6st):</label>
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

        {/* Location + Duration */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block font-medium mb-1">Verksamhet:</label>
            <select
              name="location"
              value={formData.location}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            >
              <option value="">Välj plats</option> {/* <-- Empty string = placeholder */}
              <option value="Verkstan">Verkstan</option>
              <option value="Kusten">Kusten</option>
              <option value="Konferensen">Konferensen</option>
            </select>
          </div>

          <div>
            <label className="block font-medium mb-1">Mätperiod:</label>
            <select
              name="duration"
              value={formData.duration}
              onChange={handleChange}
              className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
            >
              <option value="">Välj period</option> {/* <-- Empty string = placeholder */}
              <option value="week">En vecka</option>
              <option value="month">En månad</option>
            </select>
          </div>
        </div>

        {/* Email full width */}
        <div className="mb-6">
          <label className="block font-medium mb-1">Email:</label>
          <input
            type="email"
            name="admin_email"
            value={formData.admin_email}
            onChange={handleChange}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
          />
        </div>

        {successMessage && <p className="mt-4 text-green-600">{successMessage}</p>}
        {errorMessage && <p className="mt-4 text-red-600">{errorMessage}</p>}

        <Button label="Generate QR Code" type="submit" />
      </form>
    </PageWrapperDesktop>
  );
};

export default AdminPage;
