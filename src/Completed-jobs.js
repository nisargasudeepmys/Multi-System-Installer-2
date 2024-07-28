import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Title from "./Title.js";
import "./App.css"

function CJob() {
  const [completed_jobs, setCompleted_jobs] = useState([]);  //array of array
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/completed-jobs');
        setCompleted_jobs(response.data);
        console.log(response.data);
      } catch (error) {
        console.error('Error fetching machines:', error);
      }
    };

    fetchData();
  }, []); // Empty dependency array to run only once when the component mounts

  return (
    <div>
      <Title title="Completed Jobs" total={completed_jobs.length} button_name="completed jobs"/>
      <table className="table">
        <thead>
          <tr className="header" >
            <th className="cell">Job Id</th>
            <th className="cell">Machine Id</th>
            <th className="cell">Software Id</th>
            <th className="cell">Status</th>
            <th className="cell">Completion Time</th>
            <th className="cell">Error Message</th>
            
          </tr>
        </thead>
        <tbody>
          {completed_jobs.map(job => (
            <tr className="row" key={job.job_id}>
              <td className="cell">{job.job_id}</td>
              <td className="cell">{job.machine_id}</td>
              <td className="cell">{job.software_id}</td>
              <td className="cell">{job.status}</td>
              <td className="cell">{job.completion_time}</td>
              <td className="cell">{job.error_message}</td>
              
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CJob;

