import './duo.css';
import React, { useState } from 'react';
import axios from 'axios';

function Register() {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        confirm_password: '',
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('https://fastapi-react-app.onrender.com/auth/register/', formData);
            if (response && response.data) {
                alert(response.data.message);
                window.location.href = '/login';  // Redirect to login page after successful registration
            } else {
                alert('Unexpected response format');
            }
        } catch (error) {
            if (error.response && error.response.data) {
                alert(error.response.data.detail);  // Handle error response data
            } else {
                alert('An error occurred. Please try again later.');  // Fallback message
            }
        }
    };

    return (
        <div>
            <h1>Register</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Username"
                    onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                />
                <input
                    type="password"
                    placeholder="Password"
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                />
                <input
                    type="password"
                    placeholder="Confirm Password"
                    onChange={(e) => setFormData({ ...formData, confirm_password: e.target.value })}
                />
                <button type="submit">Register</button>
            </form>

            <div>
                <p>Already registered? <a href="/login">Login here</a></p>
            </div>
        </div>
    );
}

export default Register;
