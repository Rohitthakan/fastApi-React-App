import './dashboard.css';
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
    const [randomNumbers, setRandomNumbers] = useState([]);
    const [error, setError] = useState('');
    const [csvData, setCsvData] = useState([]);
    const [newRecord, setNewRecord] = useState({ user: '', broker: '', API_key: '', API_secret: '', pnl: '', margin: '', max_risk: '' });
    const [editIndex, setEditIndex] = useState(null);
    const [isUserMatched, setIsUserMatched] = useState(false);

    // Fetch random numbers every second
    useEffect(() => {
        const interval = setInterval(() => {
            axios.get('https://fastapi-react-app-tren.onrender.com/dashboard/random-numbers/')
                .then((response) => {
                    setRandomNumbers(response.data);
                })
                .catch((error) => {
                    console.error(error);
                });
        }, 1000);

        return () => clearInterval(interval);
    }, []);

    // Fetch CSV data
    const handleFetchCsv = async () => {
        try {
            const response = await axios.get('https://fastapi-react-app-tren.onrender.com/csv/fetch-csv/');
            setCsvData(response.data.data);
        } catch (err) {
            setError(err.response.data.detail);
        }
    };

    useEffect(() => {
        const storedUsername = localStorage.getItem('username');
        console.log(storedUsername)
        let isUserFound = false;

        for (const row of csvData) {
            if (row.user === storedUsername) {
                isUserFound = true;
                break;
            }
        }

        setIsUserMatched(isUserFound);
    }, [csvData]);

    const handlePreviousVersion = async () => {
        try {
            const response = await axios.get('https://fastapi-react-app-tren.onrender.com/csv/get-previous-version/');
            console.log(response.data); // Check the response structure

            if (Array.isArray(response.data.data)) {
                setCsvData(response.data.data);
                alert('Backup File Created Successfully')
            } else {
                alert('Expected an array, but got something else!');
            }
        } catch (err) {
            console.error(err);
            alert('Error retrieving previous version!');
        }
    };


    const [errorMessage, setErrorMessage] = useState('');

    const handleAddRecord = () => {
        if (!isUserMatched) {
            alert('You are not authorized to perform CRUD operations.');
            return;
        }
        if (Object.values(newRecord).some((value) => value === '')) {
            alert('Please fill in all fields.');
            return;
        }

        setCsvData([...csvData, newRecord]);
        setNewRecord({
            user: '',
            broker: '',
            API_key: '',
            API_secret: '',
            pnl: '',
            margin: '',
            max_risk: ''
        });
    };

    // Edit a record
    const handleEditRecord = (index) => {
        setEditIndex(index);
        setNewRecord(csvData[index]);
    };

    // Save an edited record
    const handleSaveEdit = () => {
        const updatedData = csvData.map((row, index) => (index === editIndex ? newRecord : row));
        setCsvData(updatedData);
        setEditIndex(null);
        setNewRecord({ user: '', broker: '', API_key: '', API_secret: '', pnl: '', margin: '', max_risk: '' });
    };

    // Delete a record
    const handleDeleteRecord = (index) => {
        const updatedData = csvData.filter((_, i) => i !== index);
        setCsvData(updatedData);
    };

    return (
        <div>
            <nav>
                <h3>Dashboard</h3>
                <button onClick={() => (window.location.href = '/')}>Logout</button>
            </nav>

            <h1>Random Numbers</h1>
            <table>
                <thead>
                    <tr>
                        <th>Time</th>
                        <th>Random Number</th>
                    </tr>
                </thead>
                <tbody>
                    {randomNumbers.map((entry, index) => (
                        <tr key={index}>
                            <td>{new Date(entry.timestamp).toLocaleTimeString()}</td>
                            <td>{entry.number.toFixed(2)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <h2>CSV Operations</h2>
            <button onClick={handleFetchCsv}>Fetch CSV</button>
            <button onClick={handlePreviousVersion}>Retrieve Previous Version</button>
            {error && <p style={{ color: 'red' }}>{error}</p>}

            <h2>Manage Records</h2>
            <table>
                <thead>
                    <tr>
                        <th>User</th>
                        <th>Broker</th>
                        <th>API Key</th>
                        <th>API Secret</th>
                        <th>PnL</th>
                        <th>Margin</th>
                        <th>Max Risk</th>
                        {isUserMatched && <th>Actions</th>}
                    </tr>
                </thead>
                <tbody>
                    {csvData.map((row, index) => (
                        <tr key={index}>
                            <td>{row.user}</td>
                            <td>{row.broker}</td>
                            <td>{row.API_key}</td>
                            <td>{row.API_secret}</td>
                            <td>{row.pnl}</td>
                            <td>{row.margin}</td>
                            <td>{row.max_risk}</td>
                            {isUserMatched && (
                                <td>
                                    <button onClick={() => handleEditRecord(index)}>Edit</button>
                                    <button onClick={() => handleDeleteRecord(index)}>Delete</button>
                                </td>
                            )}
                        </tr>
                    ))}
                </tbody>
            </table>

            <div>
                {isUserMatched ? (
                    <>
                        <h2>{editIndex !== null ? 'Edit Record' : 'Add New Record'}</h2>
                        <div>
                            <input
                                type="text"
                                placeholder="User"
                                value={newRecord.user}
                                onChange={(e) => setNewRecord({ ...newRecord, user: e.target.value })}
                            />
                            <input
                                type="text"
                                placeholder="Broker"
                                value={newRecord.broker}
                                onChange={(e) => setNewRecord({ ...newRecord, broker: e.target.value })}
                            />
                            <input
                                type="text"
                                placeholder="API Key"
                                value={newRecord.API_key}
                                onChange={(e) => setNewRecord({ ...newRecord, API_key: e.target.value })}
                            />
                            <input
                                type="text"
                                placeholder="API Secret"
                                value={newRecord.API_secret}
                                onChange={(e) => setNewRecord({ ...newRecord, API_secret: e.target.value })}
                            />
                            <input
                                type="text"
                                placeholder="PnL"
                                value={newRecord.pnl}
                                onChange={(e) => setNewRecord({ ...newRecord, pnl: e.target.value })}
                            />
                            <input
                                type="text"
                                placeholder="Margin"
                                value={newRecord.margin}
                                onChange={(e) => setNewRecord({ ...newRecord, margin: e.target.value })}
                            />
                            <input
                                type="text"
                                placeholder="Max Risk"
                                value={newRecord.max_risk}
                                onChange={(e) => setNewRecord({ ...newRecord, max_risk: e.target.value })}
                            />
                            {editIndex !== null ? (
                                <button onClick={handleSaveEdit}>Save</button>
                            ) : (
                                <button onClick={handleAddRecord}>Add</button>
                            )}
                        </div>
                    </>
                ) : (
                    <h2></h2>
                )}
            </div>
        </div>
    );
}

export default Dashboard;




