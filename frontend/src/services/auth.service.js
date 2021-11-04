import axios from "axios";
import { API_URL } from "../config";

const register = async (username, email, password) => {
    const response = await axios.post(API_URL + "Users/create_account", {
        username,
        email,
        password,
        is_admin: false,
        suspended: false,
    });
    localStorage.setItem("user", JSON.stringify(response.data));
    return response.data;
};

const login = async (username, password) => {
    const response = await axios.post(API_URL + "Users/login", {
        username,
        password,
    });
    localStorage.setItem("user", JSON.stringify(response.data));
    return response.data;
};

const logout = () => {
    localStorage.removeItem("user");
};

export default {
    register,
    login,
    logout,
};
