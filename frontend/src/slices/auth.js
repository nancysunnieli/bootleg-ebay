import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

import AuthService from "../services/auth.service";

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
            return thunkAPI.rejectWithValue(message);
        }
    }
);

export const login = createAsyncThunk("auth/login", async ({ username, password }, thunkAPI) => {
    console.log("login called");
    try {
        const data = await AuthService.login(username, password);
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
    console.log("persist", user);
    if (user != null) {
        thunkAPI.dispatch(login({ username: user.username, password: user.password }));
    }
});

const initialState = { isLoggedIn: false, user: null };

const authSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {
        setUser(state, action) {
            state.user = action.payload;
        },
    },
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
            window.alert("Oops login failed");
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
export const { setUser } = authSlice.actions;

export default reducer;
