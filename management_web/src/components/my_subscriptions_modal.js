import React, { useState, useEffect, useCallback } from 'react';
import { Modal, List, Button, Icon, Loader, Table, Pagination, Label, Message } from 'semantic-ui-react';
import { get_subscription, toggle_subscription_status, unsubscribe, get_reports } from '../services/api';

const MySubscriptionsModal = ({ isOpen, onClose }) => {
    const [view, setView] = useState('list'); // 'list' or 'files'
    const [selectedSub, setSelectedSub] = useState(null);
    const [loading, setLoading] = useState(false);
    const [subscriptions, setSubscriptions] = useState([]);
    const [error, setError] = useState(null);

    const [reports, setReports] = useState([]);
    const [activePage, setActivePage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const PAGE_SIZE = 8;

    const refreshList = useCallback(async () => {
        setLoading(true);
        try {
            const data = await get_subscription();
            setSubscriptions(data);
            setError(null);
        } catch (err) {
            setError("Unable to load subscription list. Please try again later.");
        } finally {
            setLoading(false);
        }
    }, []);

    const fetchReports = useCallback(async (taskId, page) => {
        setLoading(true);
        try {
            const data = await get_reports(taskId, page, PAGE_SIZE);
            setReports(data.items);
            setTotalPages(data.total_pages);
            setActivePage(data.page);
        } catch (err) {
            setError("Unable to load reports. Please try again later.");
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        if (isOpen) {
            refreshList();
            setView('list');
        }
    }, [isOpen, refreshList]);

    useEffect(() => {
        if (view === 'files' && selectedSub) {
            fetchReports(selectedSub.report_task_id, activePage);
        }
    }, [activePage, view, selectedSub, fetchReports]);

    const handleSubClick = (sub) => {
        setSelectedSub(sub);
        setActivePage(1);
        setView('files');
    };

    const handleBack = () => {
        setView('list');
        setSelectedSub(null);
        setReports([]);
    };

    const handleTogglePause = async (sub) => {
        try {
            const newStatus = !sub.is_active;
            await toggle_subscription_status(sub.report_task_id, newStatus);
            refreshList();
        } catch (err) {
            alert("Status update failed");
        }
    };

    const handleUnsubscribe = async (sub) => {
        if (window.confirm(`Are you sure you want to unsubscribe from ${sub.target_name}? This will stop generating new reports.`)) {
            try {
                await unsubscribe(sub.report_task_id);
                refreshList();
            } catch (err) {
                alert("Unsubscription failed");
            }
        }
    };

    return (
        <Modal open={isOpen} onClose={onClose} size='small' closeIcon>
            <Modal.Header>
                {view === 'files' && (
                    <Button icon='arrow left' basic circular onClick={handleBack} style={{ marginRight: '1em' }} />
                )}
                <Icon name='newspaper outline' />
                {view === 'list' ? 'My Reports' : `Report List: ${selectedSub?.target_name}`}
            </Modal.Header>

            <Modal.Content scrolling style={{ minHeight: '300px' }}>
                {error && <Message error content={error} />}

                {loading && view === 'list' ? (
                    <Loader active inline='centered'>Loading...</Loader>
                ) : view === 'list' ? (
                    <List selection divided relaxed='very'>
                        {subscriptions.length === 0 && !loading && <Message info content="Currently no reports subscribed." />}
                        {subscriptions.map(sub => (
                            <List.Item key={sub.report_task_id} onClick={() => handleSubClick(sub)}>
                                <List.Content floated='right'>
                                    <Button.Group size='mini'>
                                        <Button
                                            icon
                                            basic
                                            color={sub.is_active ? 'orange' : 'green'}
                                            onClick={(e) => { e.stopPropagation(); handleTogglePause(sub); }}
                                            title={sub.is_active ? 'Pause' : 'Resume'}
                                        >
                                            <Icon name={sub.is_active ? 'pause' : 'play'} />
                                        </Button>
                                        <Button
                                            icon
                                            basic
                                            color='red'
                                            onClick={(e) => { e.stopPropagation(); handleUnsubscribe(sub); }}
                                            title="Unsubscribe"
                                        >
                                            <Icon name='trash alternate' />
                                        </Button>
                                    </Button.Group>
                                </List.Content>

                                <List.Content>
                                    <List.Header>
                                        {sub.target_name}
                                        {sub.is_active ?
                                            <Label size='mini' color='green' circular empty style={{ marginLeft: '8px' }} /> :
                                            <Label size='mini' color='grey' style={{ marginLeft: '8px' }}>Paused</Label>
                                        }
                                    </List.Header>
                                    <List.Description>
                                        <Icon name='clock outline' /> Frequency: {sub.task_detail.frequency} |
                                        Type: <strong>{sub.task_detail.target_type.toUpperCase()}</strong>
                                    </List.Description>
                                </List.Content>
                            </List.Item>
                        ))}
                    </List>
                ) : (
                    <>
                        <Table basic='very' selectable compact>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell>Filename</Table.HeaderCell>
                                    <Table.HeaderCell textAlign='right'>Download</Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>
                            <Table.Body>
                                {loading ? (
                                    <Table.Row><Table.Cell colSpan='2' textAlign='center'><Loader active inline /></Table.Cell></Table.Row>
                                ) : reports.length === 0 ? (
                                    <Table.Row><Table.Cell colSpan='2' textAlign='center'>No report available at the moment.</Table.Cell></Table.Row>
                                ) : (
                                    reports.map(file => (
                                        <Table.Row key={file.id}>
                                            <Table.Cell>
                                                <Icon name='file excel outline' color='green' />
                                                {file.s3_key.split('/').pop()}
                                            </Table.Cell>
                                            <Table.Cell textAlign='right'>
                                                <a
                                                    href={file.download_url}
                                                    download={`${file.s3_key.split('/').pop()}`}
                                                    rel="noreferrer"
                                                >
                                                    <Button
                                                        size='mini'
                                                        circular
                                                        icon='download'
                                                        color='blue'
                                                        onClick={(e) => e.stopPropagation()}
                                                    />
                                                </a>
                                            </Table.Cell>
                                        </Table.Row>
                                    ))
                                )}
                            </Table.Body>
                        </Table>

                        {totalPages > 1 && (
                            <div style={{ textAlign: 'center', marginTop: '1.5em' }}>
                                <Pagination
                                    activePage={activePage}
                                    onPageChange={(e, { activePage }) => setActivePage(activePage)}
                                    totalPages={totalPages}
                                    size='mini'
                                />
                            </div>
                        )}
                    </>
                )}
            </Modal.Content>
            <Modal.Actions>
                <Button onClick={onClose} basic>Close</Button>
            </Modal.Actions>
        </Modal>
    );
};

export default MySubscriptionsModal;