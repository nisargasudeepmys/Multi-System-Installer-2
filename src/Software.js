import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Title from "./Title.js";
import "./App.css";

function Software() {
  const [softwares, setSoftwares] = useState([]);
  const [newSoftware, setNewSoftware] = useState({
    software_id: '',
    name: '',
    version: '',
    description: '',
    os_type: '',
    extension: ''
  });
  const [showForm, setShowForm] = useState(false);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/software');
      setSoftwares(response.data);
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching softwares:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewSoftware(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/software', newSoftware);
      fetchData();
      setNewSoftware({
        software_id: '',
        name: '',
        version: '',
        description: '',
        os_type: '',
        extension: ''
      });
      setShowForm(false);
    } catch (error) {
      console.error('Error adding software:', error);
    }
  };

  const handleDelete = async (software_id) => {
    try {
      await axios.delete(`http://localhost:5000/software/${software_id}`);
      fetchData();
    } catch (error) {
      console.error('Error deleting software:', error);
    }
  };

  return (
    <div>
      <Title title="Softwares" total={softwares.length} button_name="software" />
      <table className="table">
        <thead>
          <tr className="header">
            <th className="cell">Software Id</th>
            <th className="cell">Name</th>
            <th className="cell">Version</th>
            <th className="cell">Description</th>
            <th className="cell">OS Type</th>
            <th className="cell">Extension</th>
            <th className="cell">Action</th>
          </tr>
        </thead>
        <tbody>
          {softwares.map(software => (
            <tr className="row" key={software.software_id}>
              <td className="cell">{software.software_id}</td>
              <td className="cell">{software.name}</td>
              <td className="cell">{software.version}</td>
              <td className="cell">{software.description}</td>
              <td className="cell">{software.os_type}</td>
              <td className="cell">{software.extension}</td>
              <td className="cell">
                <button onClick={() => handleDelete(software.software_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={() => setShowForm(!showForm)}>Add Software</button>
      {showForm && (
        <form onSubmit={handleSubmit} className="form-container">
          <h2>Add New Software</h2>
          <input
            type="text"
            name="software_id"
            placeholder="Software ID"
            value={newSoftware.software_id}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="name"
            placeholder="Name"
            value={newSoftware.name}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="version"
            placeholder="Version"
            value={newSoftware.version}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="description"
            placeholder="Description"
            value={newSoftware.description}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="os_type"
            placeholder="OS Type"
            value={newSoftware.os_type}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="extension"
            placeholder="Extension"
            value={newSoftware.extension}
            onChange={handleChange}
            required
          />
          <button type="submit">Add Software</button>
        </form>
      )}
    </div>
  );
}

export default Software;
