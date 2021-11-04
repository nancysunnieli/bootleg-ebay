import axios from "axios";
import { API_URL } from "../config";

const register = (username, email, password) => {
    console.log("register");
    return axios
        .post(API_URL + "Users/CreateAccount", {
            username,
            email,
            password,
            is_admin: false,
            suspended: false,
        })
        .then((response) => {
            localStorage.setItem("user", JSON.stringify(response.data));

            return response.data;
        });
};

const login = (username, password) => {
    return axios
        .post(API_URL + "Users/Login", {
            username,
            password,
        })
        .then((response) => {
            if (response.data.accessToken) {
                localStorage.setItem("user", JSON.stringify(response.data));
            }

            return response.data;
        });
};

const logout = () => {
    localStorage.removeItem("user");
};

export default {
    register,
    login,
    logout,
};
