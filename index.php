<HTML>
<HEAD>
<TITLE>Extra Stats Parser for Logs.tf</TITLE>
</HEAD>

<BODY>

<? 
	if (isset($_GET["log"]) && !empty($_GET["log"])) {

		$logloc = "logs/" . $_GET["log"] . ".log";

		if (file_exists($logloc)) {

			$execstr = '/usr/bin/python extrastats.py ' . $logloc;
			//var_dump(utf8_encode(shell_exec($execstr)), true);
			$data = json_decode(shell_exec($execstr), true);

			if (!empty($data)) {

				foreach ($data as $key => $val) {
					// key 0 = damaged given, key 1 = damaged received 
					$type = (!$key) ? "Damaged Given" : "Damaged Received";
					?>
					<h3><? echo $type; ?></h3>
					<?
					foreach ($val[1] as $player => $stats) {
					?>
						<table class="<? echo $stats['pdata']['team']; ?>-team">
							<tr>
								<th colspan="2"><? echo $player; ?></th>
							</tr>
					<?
						foreach($stats['players'] as $pname => $pstats) {
							?>
							<tr>
								<td><? echo $pname; ?></td>
								<td><? echo $pstats['da']; ?></td>
							</tr>	
							<?
						}
					}
					?>
						</table>
					<?
				}
			}
		}
	}

?>

</BODY>
</HTML>