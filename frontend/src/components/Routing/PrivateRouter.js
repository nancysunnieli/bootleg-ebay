// This is used to determine if a user is authenticated and
// if they are allowed to visit the page they navigated to.

// If they are: they proceed to the page
// If not: they are redirected to the login page.
import React from "react";
import { Redirect, Route } from "react-router-dom";
import { useSelector } from "react-redux";
import { ROLE_ADMIN } from "../../constants";

const PrivateRoute = ({ component: Component, roles, ...routeprops }) => {
    const { isLoggedIn, isAdmin } = useSelector((state) => state.auth);
    console.log("IsAdmin", isAdmin);
    return (
        <Route
            {...routeprops}
            render={(props) => {
                if (!isLoggedIn) return <Redirect to={{ pathname: "/login" }} />;
                if (roles.includes(ROLE_ADMIN) && !isAdmin)
                    return <Redirect to={{ pathname: "/notok" }} />;
                else return <Component {...props} />;
            }}
        />
    );
};

export default PrivateRoute;
