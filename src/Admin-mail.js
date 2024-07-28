import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Title from "./Title.js";
import "./App.css";

function Mail() {
  const [adminMail, setAdminMail] = useState([]);
  const [newMail, setNewMail] = useState({
    email_id: '',
    smtp_server: '',
    port: '',
    api_token: '',
  });
  const [showForm, setShowForm] = useState(false);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/admin-mail');
      setAdminMail(response.data);
    } catch (error) {
      console.error('Error fetching mail:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleDelete = async (email_id) => {
    try {
      await axios.delete(`http://localhost:8000/admin-mail/${email_id}`);
      fetchData();  // Refresh the data
    } catch (error) {
      console.error('Error deleting admin mail:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewMail((prevMail) => ({
      ...prevMail,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/admin-mail', newMail);
      setNewMail({
        email_id: '',
        smtp_server: '',
        port: '',
        api_token: '',
      });
      setShowForm(false);
      fetchData();  // Refresh the data
    } catch (error) {
      console.error('Error adding new admin mail:', error);
    }
  };

  return (
    <div>
      <Title title="Admin Configuration" total={adminMail.length} button_name="mail" />
      <table className="table">
        <thead>
          <tr className="header">
            <th className="cell">Email Id</th>
            <th className="cell">SMTP Server</th>
            <th className="cell">Port</th>
            <th className="cell">API Token</th>
            <th className="cell">Actions</th>
          </tr>
        </thead>
        <tbody>
          {adminMail.map((mail) => (
            <tr className="row" key={mail.email_id}>
              <td className="cell">{mail.email_id}</td>
              <td className="cell">{mail.smtp_server}</td>
              <td className="cell">{mail.port}</td>
              <td className="cell">{mail.api_token}</td>
              <td className="cell">
                <button onClick={() => handleDelete(mail.email_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={() => setShowForm(!showForm)}>Add Admin Mail</button>
      {showForm && (
      <form onSubmit={handleSubmit} className="form-container">
        <h2>Add New Admin Mail</h2>
        <input
          type="text"
          name="email_id"
          placeholder="Email ID"
          value={newMail.email_id}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="smtp_server"
          placeholder="SMTP Server"
          value={newMail.smtp_server}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="port"
          placeholder="Port"
          value={newMail.port}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="api_token"
          placeholder="API Token"
          value={newMail.api_token}
          onChange={handleChange}
          required
        />
        <button type="submit">Add Admin Mail</button>
      </form>
      )}
    </div>
    
  );
}

export default Mail;
