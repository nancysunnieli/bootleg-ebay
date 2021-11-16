import Spinner from "react-bootstrap/Spinner";

export default function Loading() {
    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                height: "80vh",
            }}
        >
            <h1>Loading</h1>
            <br />
            <Spinner animation="grow" variant="success" />
        </div>
    );
}
