import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import { useState } from "react";
import { register } from "../../slices/auth";
import { useDispatch, useSelector } from "react-redux";
import { Redirect } from "react-router-dom";
const Register = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [username, setUsername] = useState("");
    const [isAdmin, setIsAdmin] = useState(false);
    const dispatch = useDispatch();
    const { isLoggedIn } = useSelector((state) => state.auth);

    const registerUser = (e) => {
        e.preventDefault();
        dispatch(register({ email, password, username, isAdmin }));
    };
    if (isLoggedIn) return <Redirect to={{ pathname: "/home" }} />;
    return (
        <div>
            <h1>Register</h1>
            <Form onSubmit={registerUser}>
                <Form.Group className="mb-3" controlId="formBasicEmail">
                    <Form.Label>Email address</Form.Label>
                    <Form.Control
                        type="email"
                        placeholder="Enter email"
                        value={email}
                        onChange={({ target: { value } }) => setEmail(value)}
                    />
                </Form.Group>

                <Form.Group className="mb-3" controlId="formBasicUsername">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        type="input"
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

                <Form.Group className="mb-3" controlId="formBasicCheckbox">
                    <Form.Check
                        type="checkbox"
                        label="Is Admin Account?"
                        onChange={(event) => setIsAdmin(event.target.checked)}
                    />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Register
                </Button>
            </Form>
        </div>
    );
};

export default Register;
