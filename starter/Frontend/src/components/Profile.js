import React, { useEffect } from "react";
import { useAuth0, withAuthenticationRequired } from "@auth0/auth0-react";
import Loading from './Loading';

const Profile = () => {
  const { user, getAccessTokenSilently } = useAuth0();

  useEffect(() => {
    const getUserToken = async () => {
      try {
        const accessToken = await getAccessTokenSilently({
          audience: `boardgameforum`
        });
        console.log(accessToken);
        sessionStorage.setItem("token", accessToken);
      } catch (e) {
        console.log(e.message);
      }
    };

    getUserToken();
  });

  return (
    <div>
      <div className="row align-items-center profile-header">
        <div className="col-md-2 mb-3">
          <img
            src={user.picture}
            alt="Profile"
            className="rounded-circle img-fluid profile-picture mb-3 mb-md-0"
          />
        </div>
        <div className="col-md text-center text-md-left">
          <h2>{user.name}</h2>
          <p className="lead text-muted">{user.email}</p>
        </div>
      </div>
      <div className="row">
        <pre className="col-12 text-light bg-dark p-4">
          {JSON.stringify(user, null, 2)}
        </pre>
      </div>
    </div>
  );
};

export default withAuthenticationRequired(Profile, {
  returnTo: () => window.location.hash.substr(1),
  onRedirecting: () => <Loading />,
});