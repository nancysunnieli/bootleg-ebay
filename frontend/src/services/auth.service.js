import axios from "axios";
import { API_URL } from "../config";

const register = async (username, email, password, isAdmin) => {
    const response = await axios.post(API_URL + "users/user", {
        username,
        email,
        password,
        is_admin: isAdmin,
        suspended: false,
    });
    localStorage.setItem("user", JSON.stringify(response.data));
    return response.data;
};

const login = async (username, password) => {
    const response = await axios.post(API_URL + "users/login", {
        username,
        password,
    });
    localStorage.setItem("user", JSON.stringify(response.data));
    console.log("login", response.data);
    return response.data;
    // const user = JSON.parse(localStorage.getItem("user"));
    // return user;
};

const logout = () => {
    localStorage.removeItem("user");
};

const AuthService = {
    register,
    login,
    logout,
};

export default AuthService;
