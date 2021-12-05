import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { toast } from "react-toastify";

import AuthService from "../services/auth.service";
import { getItemsFromCart } from "./cart";

export const register = createAsyncThunk(
    "auth/register",
    async ({ username, email, password, isAdmin }, thunkAPI) => {
        try {
            console.log("register thunk");
            const data = await AuthService.register(username, email, password, isAdmin);
            //   thunkAPI.dispatch(setMessage(response.data.message));
            return { user: data };
        } catch (error) {
            const message = error.toString();
            //   thunkAPI.dispatch(setMessage(message));
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const login = createAsyncThunk("auth/login", async ({ username, password }, thunkAPI) => {
    console.log("login called");
    try {
        const data = await AuthService.login(username, password);
        await new Promise((resolve) => setTimeout(resolve, 1000));
        thunkAPI.dispatch(getItemsFromCart({ user_id: data.user_id }));
        return { user: data };
    } catch (error) {
        const message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
        //   thunkAPI.dispatch(setMessage(message));
        return thunkAPI.rejectWithValue(message);
    }
});

export const logout = createAsyncThunk("auth/logout", async () => {
    console.log("Logging out");
    await AuthService.logout();
});

export const checkLocalLogin = createAsyncThunk("auth/checkLocalLogin", async (_, thunkAPI) => {
    const user = JSON.parse(localStorage.getItem("user"));
    thunkAPI.dispatch(login({ username: user?.username, password: user?.password }));
});

const initialState = { isLoggedIn: null, user: null, isAdmin: false };

const authSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {
        setUser(state, action) {
            console.log("Set User data", action.payload);
            state.user = action.payload;
        },
    },
    extraReducers: {
        [register.fulfilled]: (state, action) => {
            console.log("action", action.payload);
            state.isLoggedIn = true;
            state.user = action.payload.user;
            state.isAdmin = action.payload.user.is_admin;
        },
        [register.rejected]: (state, action) => {
            state.isLoggedIn = false;
        },
        [login.fulfilled]: (state, action) => {
            state.isLoggedIn = true;
            state.user = action.payload.user;
            state.isAdmin = action.payload.user.is_admin;
        },
        [login.rejected]: (state, action) => {
            console.log("login failed");
            toast.error("Login failed, error: " + action.payload);
            state.isLoggedIn = false;
            state.user = null;
        },
        [logout.fulfilled]: (state, action) => {
            state.isLoggedIn = false;
            toast.success("Login success!");
            state.user = null;
        },
    },
});

const { reducer } = authSlice;
export const { setUser } = authSlice.actions;

export default reducer;
