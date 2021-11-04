import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { useState } from "react";
import { login } from "../../slices/auth";
import { useDispatch, useSelector } from "react-redux";
import { Redirect } from "react-router-dom";

const Login = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const { isLoggedIn } = useSelector((state) => state.auth);
    const dispatch = useDispatch();
    const loginUser = (e) => {
        e.preventDefault();
        dispatch(login({ username, password }));
    };

    if (isLoggedIn) return <Redirect to={{ pathname: "/home" }} />;

    return (
        <div>
            <h1>Login</h1>
            <Form onSubmit={loginUser}>
                <Form.Group className="mb-3">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        placeholder="Enter username"
                        value={username}
                        onChange={({ target: { value } }) => setUsername(value)}
                    />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicPassword">
                    <Form.Label>Password</Form.Label>
                    <Form.Control
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={({ target: { value } }) => setPassword(value)}
                    />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Login
                </Button>
            </Form>
        </div>
    );
};

export default Login;
