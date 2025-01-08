import React, { useState } from 'react';
import Login from './Login'; // Import Login component
import SignUp from './SignUp'; // Import SignUp component

const Home = () => {
  const [isSignUp, setIsSignUp] = useState(false); // State to toggle between login and signup

  return (
    <div className="home-container">
      <h1>LiveSync</h1>

      {isSignUp ? (
        // Show SignUp form when isSignUp is true
        <SignUp />
      ) : (
        // Show Login form when isSignUp is false
        <Login />
      )}

      <p>
        {isSignUp ? (
          <>
            Already have an account?{' '}
            <a href="#" onClick={() => setIsSignUp(false)}>
              Log in here
            </a>
          </>
        ) : (
          <>
            Don't have an account?{' '}
            <a href="#" onClick={() => setIsSignUp(true)}>
              Sign up here
            </a>
          </>
        )}
      </p>
    </div>
  );
};

export default Home;
