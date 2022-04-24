import React from "react";
import { useAuth0 } from '@auth0/auth0-react';

const { error } = useAuth0();
const Error = () => (
  <div className="spinner">
    <p>Oops... {error.message}</p>;
  </div>
);

export default Error;