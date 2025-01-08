import React, { useState } from "react";
import API from "../../utils/api";

const SignUp = () => {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        const formData = {
          email: email,
          password: password
        };
      
        try {
          const response = await API.post("/auth/", formData, {
            headers: {
              'Content-Type': 'application/json', 
            }
          });
          console.log(response);

          const { access_token } = response.data;
          localStorage.setItem("token", access_token);
          setError("");
          alert("Sign up successful!");
        } catch (err) {
          console.error(err);
          if (err.response) {
            console.error('Error response:', err.response.data); 
          }
          setError("Invalid credentials, please try again.");
        }
      };



    return(
    <div className="signup-container">
      <form onSubmit={handleSubmit} className="signup-form">
        <h2>Sign Up</h2>
        {error && <p className="error-message">{error}</p>}

        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="signup-button">
          Sign Up
        </button>
      </form>
    </div>
    );
}

export default SignUp;