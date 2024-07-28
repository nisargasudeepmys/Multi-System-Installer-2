import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Title from "./Title.js";
import "./App.css";

function SJob() {
  const [scheduledJobs, setScheduledJobs] = useState([]);
  const [newJob, setNewJob] = useState({
    job_id: '',
    machine_id: '',
    software_id: '',
    scheduled_time: ''
  });
  const [showForm, setShowForm] = useState(false);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/scheduled-jobs');
      setScheduledJobs(response.data);
      console.log(response.data);
    } catch (error) {
      console.error('Error fetching scheduled jobs:', error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewJob(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Convert the scheduled_time to IST
    const date = new Date(newJob.scheduled_time);
    const offset = 5.5 * 60 * 60 * 1000; // IST offset
    const istDate = new Date(date.getTime() + offset);
    const formattedJob = {
      ...newJob,
      scheduled_time: istDate.toISOString().slice(0, 19).replace('T', ' ')
    };

    try {
      await axios.post('http://localhost:5000/scheduled-jobs', formattedJob);
      fetchData();
      setNewJob({
        job_id: '',
        machine_id: '',
        software_id: '',
        scheduled_time: ''
      });
      setShowForm(false);
    } catch (error) {
      console.error('Error adding scheduled job:', error);
    }
  };

  const handleDelete = async (job_id) => {
    try {
      await axios.delete(`http://localhost:5000/scheduled-jobs/${job_id}`);
      fetchData();
    } catch (error) {
      console.error('Error deleting scheduled job:', error);
    }
  };

  return (
    <div>
      <Title title="Scheduled Jobs" total={scheduledJobs.length} button_name="scheduled job" />
      <table className="table">
        <thead>
          <tr className="header">
            <th className="cell">Job Id</th>
            <th className="cell">Machine Id</th>
            <th className="cell">Software Id</th>
            <th className="cell">Time</th>
            <th className="cell">Action</th>
          </tr>
        </thead>
        <tbody>
          {scheduledJobs.map(job => (
            <tr className="row" key={job.job_id}>
              <td className="cell">{job.job_id}</td>
              <td className="cell">{job.machine_id}</td>
              <td className="cell">{job.software_id}</td>
              <td className="cell">{job.scheduled_time}</td>
              <td className="cell">
                <button onClick={() => handleDelete(job.job_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={() => setShowForm(!showForm)}>Add Job</button>
      {showForm && (
        <form onSubmit={handleSubmit} className="form-container">
          <h2>Add New Scheduled Job</h2>
          <input
            type="text"
            name="job_id"
            placeholder="Job ID"
            value={newJob.job_id}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="machine_id"
            placeholder="Machine ID"
            value={newJob.machine_id}
            onChange={handleChange}
            required
          />
          <input
            type="text"
            name="software_id"
            placeholder="Software ID"
            value={newJob.software_id}
            onChange={handleChange}
            required
          />
          <input
            type="datetime-local"
            name="scheduled_time"
            value={newJob.scheduled_time}
            onChange={handleChange}
            required
          />
          <button type="submit">Add Scheduled Job</button>
        </form>
      )}
    </div>
  );
}

export default SJob;
