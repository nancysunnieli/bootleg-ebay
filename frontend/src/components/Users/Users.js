import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useHistory, useParams } from "react-router-dom";
import { getUser, getUserBids, unsuspendAccount } from "../../slices/users";
import Loading from "../Loading/Loading";
import Spinner from "react-bootstrap/Spinner";
import Button from "react-bootstrap/Button";
import Table from "react-bootstrap/Table";
import { suspendAccount } from "../../slices/users";

export default function Users() {
    const auth = useSelector((state) => state.auth);
    const is_admin = auth.user.is_admin;
    const { user, isGetUserLoading, userBids, isGetUserBidsLoading } = useSelector(
        (state) => state.users
    );
    let { user_id } = useParams();
    user_id = parseInt(user_id);
    const dispatch = useDispatch();
    const history = useHistory();
    useEffect(() => {
        const init = () => {
            dispatch(getUser({ user_id }));
            dispatch(getUserBids({ user_id }));
        };
        init();
    }, []);

    if (isGetUserLoading) return <Loading />;

    const handleSuspend = () => {
        if (user.suspended) {
            dispatch(unsuspendAccount({ user_id }));
        } else {
            dispatch(suspendAccount({ user_id }));
        }
    };

    const { username, total_rating, number_of_ratings, suspended } = user;
    let tbody = userBids.flatMap((ub, i) => {
        let isEnded = ub.auction.end_time * 1000 < new Date().getTime();
        return ub.user_bids.map((bid, j) => (
            <tr key={`${bid.bid_id}_${i}_${j}`}>
                <td>{ub.item.name}</td>
                <td>{bid.price}</td>
                <td key={bid.bid_time}>{new Date(bid.bid_time * 1000).toLocaleString()}</td>
                <td>{isEnded ? "Ended" : new Date(ub.auction.end_time * 1000).toLocaleString()}</td>
                <td>
                    <Button onClick={() => history.push(`/items/${ub.item._id}`)}>View</Button>
                </td>
            </tr>
        ));
    });
    tbody.sort((a, b) => parseFloat(b.props.children[2].key) - parseFloat(a.props.children[2].key));

    return (
        <div>
            <h1>{username}</h1>
            <h5>User Rating: {(total_rating / number_of_ratings || 0).toFixed(1)}★</h5>
            {is_admin && (
                <Button onClick={handleSuspend} variant="warning">
                    {suspended ? "Unsuspend" : "Suspend"}
                </Button>
            )}
            <br />
            <h2>Status</h2>
            <h4>Is Suspended: {suspended ? "True" : "False"}</h4>
            <br />
            <h2>User Bids</h2>
            {isGetUserBidsLoading ? (
                <Spinner animation="grow" variant="success" />
            ) : (
                <div style={{ position: "relative" }}>
                    <Table striped hover responsive="sm">
                        <thead>
                            <tr>
                                <th>Item Name</th>
                                <th>Bid Price</th>
                                <th>Bid Time</th>
                                <th>Auction Ends On</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>{tbody}</tbody>
                    </Table>
                </div>
            )}
        </div>
    );
}
