import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/esm/Container";
import { useDispatch, useSelector } from "react-redux";
import { useHistory } from "react-router-dom";
import SellerItems from "./SellerItems";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import UserBids from "./UserBids";
const Home = () => {
    const { user } = useSelector((state) => state.auth);
    const history = useHistory();
    const dispatch = useDispatch();

    return (
        <div>
            <h1>Home</h1>
            <h3>Welcome {user.username}!</h3>
            <br />
            <Row>
                <Col md="auto">
                    <h3>Your Items</h3>
                </Col>
                <Col>
                    <Button onClick={() => history.push("/create_item")}>
                        + Create a new Item
                    </Button>
                </Col>
            </Row>
            <br />
            <Row>
                <Col>
                    <SellerItems />
                </Col>
            </Row>
            <br />
            <Row>
                <Col>
                    <h3>Your Bids</h3>
                </Col>
            </Row>
            <br />
            <Row>
                <Col>
                    <UserBids />
                </Col>
            </Row>
        </div>
    );
};

export default Home;
