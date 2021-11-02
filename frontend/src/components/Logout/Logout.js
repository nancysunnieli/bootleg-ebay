import { useCallback } from "react";
import { useSelector, useDispatch } from "react-redux";
import { Redirect } from "react-router-dom";
import { logout } from "../../slices/auth";

const Logout = () => {
    const { isLoggedIn } = useSelector((state) => state.auth);
    const dispatch = useDispatch();

    if (isLoggedIn) {
        dispatch(logout());
    }

    return <Redirect to={{ pathname: "/login" }} />;
};

export default Logout;
