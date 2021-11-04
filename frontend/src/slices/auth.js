import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { ROLE_ADMIN, ROLE_USER } from "../constants";

import AuthService from "../services/auth.service";

const user = JSON.parse(localStorage.getItem("user"));

export const register = createAsyncThunk(
    "auth/register",
    async ({ username, email, password }, thunkAPI) => {
        try {
            console.log("register thunk");
            const response = await AuthService.register(username, email, password);
            //   thunkAPI.dispatch(setMessage(response.data.message));
            return response.data;
        } catch (error) {
            const message = error.toString();
            //   thunkAPI.dispatch(setMessage(message));
            return thunkAPI.rejectWithValue();
        }
    }
);

export const login = createAsyncThunk("auth/login", async ({ email, password }, thunkAPI) => {
    try {
        // const data = await AuthService.login(email, password);
        // return { user: data };
        console.log("mocking login flow", email, password);
        return {
            user: {
                roles: [ROLE_USER],
                id: "1",
                username: "yvesshum",
                password: "123",
                email: "yvesshum1210@gmail.com",
                suspended: false,
            },
        };
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
// const initialState = {
//     user: {
//         roles: [ROLE_USER],
//     },
//     isAdmin: false,
//     isLoggedIn: true,
// };

const authSlice = createSlice({
    name: "auth",
    initialState,
    extraReducers: {
        [register.fulfilled]: (state, action) => {
            state.isLoggedIn = true;
            console.log("payload", action.payload);
            // state.user = action.payload.user;
            // state.isAdmin = action.payload.user.roles.includes(ROLE_ADMIN);
        },
        [register.rejected]: (state, action) => {
            state.isLoggedIn = false;
        },
        [login.fulfilled]: (state, action) => {
            state.isLoggedIn = true;
            state.user = action.payload.user;
            state.isAdmin = action.payload.user.roles.includes(ROLE_ADMIN);
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
