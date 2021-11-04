import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

import AuthService from "../services/auth.service";

const user = JSON.parse(localStorage.getItem("user"));

export const register = createAsyncThunk(
    "auth/register",
    async ({ username, email, password }, thunkAPI) => {
        try {
            console.log("register thunk");
            const data = await AuthService.register(username, email, password);
            //   thunkAPI.dispatch(setMessage(response.data.message));
            return { user: data };
        } catch (error) {
            const message = error.toString();
            //   thunkAPI.dispatch(setMessage(message));
            return thunkAPI.rejectWithValue();
        }
    }
);

export const login = createAsyncThunk("auth/login", async ({ username, password }, thunkAPI) => {
    try {
        const data = await AuthService.login(username, password);
        return { user: data };
    } catch (error) {
        const message =
            (error.response && error.response.data && error.response.data.message) ||
            error.message ||
            error.toString();
        //   thunkAPI.dispatch(setMessage(message));
        return thunkAPI.rejectWithValue();
    }
});

export const logout = createAsyncThunk("auth/logout", async () => {
    await AuthService.logout();
});

const initialState = user ? { isLoggedIn: true, user } : { isLoggedIn: false, user: null };

const authSlice = createSlice({
    name: "auth",
    initialState,
    extraReducers: {
        [register.fulfilled]: (state, action) => {
            console.log("action", action.payload);
            state.isLoggedIn = true;
            state.user = action.payload.user;
            state.isAdmin = action.payload.is_admin;
        },
        [register.rejected]: (state, action) => {
            state.isLoggedIn = false;
        },
        [login.fulfilled]: (state, action) => {
            state.isLoggedIn = true;
            state.user = action.payload.user;
            state.isAdmin = action.payload.is_admin;
        },
        [login.rejected]: (state, action) => {
            state.isLoggedIn = false;
            state.user = null;
        },
        [logout.fulfilled]: (state, action) => {
            state.isLoggedIn = false;
            state.user = null;
        },
    },
});

const { reducer } = authSlice;
export default reducer;
