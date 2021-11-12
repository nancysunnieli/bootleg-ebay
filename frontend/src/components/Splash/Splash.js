import Spinner from "react-bootstrap/Spinner";

export default function Splash() {
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
            <h1>Bootleg Ebay</h1>
            <br />
            <Spinner animation="grow" variant="primary" />
        </div>
    );
}
