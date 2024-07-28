import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './Inventory.css';

function Inventory() {
  const [tables, setTables] = useState([]);
  const [data, setData] = useState([]);
  const [selectedTable, setSelectedTable] = useState('');

  useEffect(() => {
    // Fetch the list of tables
    axios.get('/tables')
      .then(response => {
        setTables(response.data);
      })
      .catch(error => {
        console.error('Error fetching tables:', error);
      });
  }, []);

  const handleTableClick = (table) => {
    // Clear previous data and set selected table
    setSelectedTable(table);
    setData([]); // Clear the data first

    // Fetch data for the selected table
    axios.get(`/${table}`)
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error(`Error fetching data for table ${table}:`, error);
      });
  };

  return (
    <div className="inventory-app">
      <div className="inventory-header">
        <h2>Software Inventory</h2>
      </div>
      <div className="inventory-main">
        <div className="inventory-sidebar">
          <h3>Client Machines</h3>
          <ul>
            {tables.map(table => (
              <li key={table} onClick={() => handleTableClick(table)} className={selectedTable === table ? 'inventory-active' : ''}>
                <i className='fas fa-desktop'></i> {table}
              </li>
            ))}
          </ul>
        </div>
        <div className="inventory-content">
          {selectedTable && (
            <>
              <h2>Data for Client Machine: {selectedTable}</h2>
              <table className="inventory-table">
                <thead>
                  <tr className='.custom-header'>
                    {data.length > 0 && Object.keys(data[0]).map((key) => (
                      <th className='.custom-cell' key={key}>{key} </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.map((row, index) => (
                    <tr className='.custom-row' key={index}>
                      {Object.values(row).map((value, idx) => (
                        <td className='.custom-cell' key={idx}>{value}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Inventory;
