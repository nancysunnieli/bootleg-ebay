import moment from "moment";
import { useEffect, useState } from "react";
import Badge from "react-bootstrap/Badge";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import Form from "react-bootstrap/Form";
import Image from "react-bootstrap/Image";
import ProgressBar from "react-bootstrap/ProgressBar";
import Row from "react-bootstrap/Row";
import Table from "react-bootstrap/Table";
import { useDispatch, useSelector } from "react-redux";
import { useHistory, useParams } from "react-router-dom";
import { clearItem, getItem } from "../../slices/items";
import Loading from "../Loading/Loading";
import NotFound from "../NotFound/NotFound";
import ReportModal from "./ReportItemModal";

export default function Item() {
    const { item_id } = useParams();
    const dispatch = useDispatch();
    const { user } = useSelector((state) => state.auth);
    const history = useHistory();
    const [reportModalVisible, setReportModalVisible] = useState(false);
    const { item, isGetItemLoading } = useSelector((state) => state.items);
    useEffect(() => {
        dispatch(getItem({ item_id }));

        return () => {
            dispatch(clearItem());
        };
    }, []);

    if (isGetItemLoading) {
        return <Loading />;
    }

    if (item == null) {
        return <NotFound />;
    }

    const {
        _id,
        category,
        description,
        isFlagged,
        name,
        photos,
        quantity,
        sellerID,
        shipping,
        watchlist,
    } = item.item;
    const viewAuction = () => {
        history.push(`/auctions/${item.auction[0].auction_id}`);
    };

    return (
        <div>
            <Container style={{ width: "80%", marginBottom: "2rem" }}>
                <Row>
                    <Col>
                        <Image
                            src="https://picsum.photos/1000"
                            style={{
                                width: "30em",
                                height: "auto",
                                display: "block",
                            }}
                        />
                    </Col>
                    <Col>
                        <h1>{name}</h1>
                        <h4>{description}</h4>

                        <Row>
                            {category.map((c, i) => (
                                <Col md="auto" key={i}>
                                    <Badge key={i} bg="primary">
                                        {c}
                                    </Badge>
                                </Col>
                            ))}
                        </Row>
                        <br />
                        {item.auction.length > 0 && (
                            <Row>
                                <Button onClick={viewAuction}>Auction Happening Now!</Button>
                            </Row>
                        )}
                        <br />
                        <Row>
                            <Button variant="danger" onClick={() => setReportModalVisible(true)}>
                                Report Item
                            </Button>
                        </Row>
                    </Col>
                </Row>
                <br />
                <h3>Past Auctions</h3>
                <Row>
                    <Table striped hover responsive="sm">
                        <thead>
                            <tr>
                                <th>Bidder</th>
                                <th>Bid Price</th>
                                <th>Timestamp</th>
                            </tr>
                        </thead>
                        {/* <tbody>{tbody}</tbody> */}
                    </Table>
                </Row>
            </Container>
            <ReportModal
                show={reportModalVisible}
                item_id={_id}
                handleClose={() => setReportModalVisible(false)}
            />
        </div>
    );
}
