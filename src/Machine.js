import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Title from "./Title";
import "./App.css";

function Machine() {
  const [machines, setMachines] = useState([]);
  const [newMachine, setNewMachine] = useState({
    machine_id: '',
    username: '',
    ip_address: '',
    port_no: '',
    machine_type: '',
    os_type: '',
    email: '',
    path: '',
    password: ''
  });
  const [showForm, setShowForm] = useState(false);
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/machines');
      setMachines(response.data);
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching machines:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewMachine((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleAddMachine = async () => {
    try {
      const response = await axios.post('http://localhost:5000/machines', newMachine);
      console.log(response.data);
      setMachines((prevMachines) => [...prevMachines, newMachine]);
      setNewMachine({
        machine_id: '',
        username: '',
        ip_address: '',
        port_no: '',
        machine_type: '',
        os_type: '',
        email: '',
        path: '',
        password: ''
      });
      setShowForm(false);
    } catch (error) {
      console.error('Error adding machine:', error);
    }
  };

  const handleDeleteMachine = async (machine_id) => {
    try {
      const response = await axios.delete(`http://localhost:5000/machines/${machine_id}`);
      console.log(response.data);
      setMachines((prevMachines) => prevMachines.filter(machine => machine.machine_id !== machine_id));
    } catch (error) {
      console.error('Error deleting machine:', error);
    }
  };

  

  return (
    <div>
      <Title title="Machines" total={machines.length} button_name="Machine" />
      <table className="table">
        <thead>
          <tr className="header">
            <th className="cell">Id</th>
            <th className="cell">Username</th>
            <th className="cell">Ip Address</th>
            <th className="cell">Machine Type</th>
            <th className="cell">OS Type</th>
            <th className="cell">Email</th>
            <th className="cell">Path</th>
            <th className="cell">Action</th>
          </tr>
        </thead>
        <tbody>
          {machines.map(machine => (
            <tr className="row" key={machine.machine_id}>
              <td className="cell">{machine.machine_id}</td>
              <td className="cell">{machine.username}</td>
              <td className="cell">{machine.ip_address}</td>
              <td className="cell">{machine.machine_type}</td>
              <td className="cell">{machine.os_type}</td>
              <td className="cell">{machine.email}</td>
              <td className="cell">{machine.path}</td>
              <td className="cell"><button onClick={() => handleDeleteMachine(machine.machine_id)}>Delete</button></td>
            </tr>
          ))}
        </tbody>
      </table>
      
      <button onClick={() => setShowForm(!showForm)}>Add Machines</button>
      {showForm && (
        <div className="form-container">
          <h3>Add New Machine</h3>   
          <input type="text" name="machine_id" value={newMachine.machine_id} onChange={handleInputChange} placeholder="Machine ID" />
          <input type="text" name="username" value={newMachine.username} onChange={handleInputChange} placeholder="Username" />
          <input type="text" name="ip_address" value={newMachine.ip_address} onChange={handleInputChange} placeholder="IP Address" />
          <input type="text" name="port_no" value={newMachine.port_no} onChange={handleInputChange} placeholder="Port Number" />
          <input type="text" name="machine_type" value={newMachine.machine_type} onChange={handleInputChange} placeholder="Machine Type" />
          <input type="text" name="os_type" value={newMachine.os_type} onChange={handleInputChange} placeholder="OS Type" />
          <input type="text" name="email" value={newMachine.email} onChange={handleInputChange} placeholder="Email" />
          <input type="text" name="path" value={newMachine.path} onChange={handleInputChange} placeholder="Path" />
          <input type="password" name="password" value={newMachine.password} onChange={handleInputChange} placeholder="Password" />
          <button onClick={handleAddMachine}>Add Machine</button>
        </div>
      )}

      
    </div>
  );
}

export default Machine;
